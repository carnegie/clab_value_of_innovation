#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:09:41 2020

@author: kcaldeira and Candise Henry
"""

"""
This is the main set of routines for the DICEeq model.

The name DICEeq was meant to evoke the idea of differential equations (diffeqs)
and also DICE-equivalent, because the goal here is to make a version of DICE
that is based on differential equations rather than difference equations.

Further, this version separates these time intervals:
    time step
    decision time points
    driving data
    
"""

"""
Important differences from DICE model.

The original DICE model had numbers in units of GtC, GtCO2, USD, trillions USD,
millions of people, per capita, per 5-year period, per year.

One of the first things done is to normalize units.

Somewhat aritrarily, we will choose to use tC (tons of carbon), USD, people,
years.
 

The variable <info> contains all of the info and functions needed
to compute time derivatives.

<info> variables:
    gBack -- rate of cost-improvement of backstop technology (fraction per year)
    expcost2 -- exponent describing how abatement cost scales with abatement fraction
    t -- time in years from start of problem (not calendar year !)
    
<info> functions:
    L[t] -- population (people)
    sigma[t] -- carbon emissions per unit unabated economic output (tC/USD)
    miu[t] -- actions taken by the agent [actions are at specified times, this
              function step functions at each of the decision points
    al[t] -- total factor productivity, in units of amount of output in USD of 1 person
             with 1 USD of capital.
    
NOTE: If <info> is local in an environment, it is called <info>, but
      we try to keep it global to avoid shadowing issues with 
    
The variable <state> contains all of the information that defines the state.

<state> variables:
    k -- capital stock
    
"""
    
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:35:42 2019
Code for non-cooperative Nash equilibrium optimization of dual actor DICE model 
with resource transfer.
Similar to Nordhaus RICE method.
Optimize x action vector: (1) % CO2 reduction, (2) % allocation, as both dollar
transfer amount (TRANSFER) and % of mitigation (ALLOC), from actor A to actor B.
Only 1 econ function (instead of 2, one for each actor).
Use with Process_Inputs_Nash.py.
@author: candise henry
"""

import numpy as np
import itertools as it
import utils
import copy
# from plot_utilities import *
from scipy import interpolate
import random
#import copy
import os
import sys
# Specify path where MIDACO files are stored depending on OS
if (os.name != "nt"):
    sys.path.insert(0, '/mnt/c/Users/clh19/Documents/Carnegie/Energy_Access/DICE_Code/MIDACO6.0') # Linux (Candise Henry)
else:
    sys.path.insert(0, 'C:/Users/kcaldeira/Documents/MIDACO/Windows') # Windows
import midaco_key as midaco
from io_utilities import pickle_results,filter_dic 
import datetime

########################################################################
################### FUNCTIONS & OPTIMIZATION PROBLEM ###################
########################################################################

#%%

# see below for list of variables

def initStateInfo(kwargs):
    # creates <state> and <info>
    state = {}  # state variables
    info = {} # driving variables and diagnostic info
    
   #---------------------------------------------------------------------------
   #------- Unpack keyword arguments ------------------------------------------
   #---------------------------------------------------------------------------

      #------- Process information about time -------- ---------------------------
      #-----> integration time step  
    
    if 'dt' in kwargs.keys():
        dt = kwargs['dt']
    else:
        dt = 1.0
    info['dt'] = dt 
  
    #-----> miuDecisionTimes 
    
    if 'miuDecisionTimes' in kwargs.keys():
        info['miuDecisionTimes'] = kwargs['miuDecisionTimes']
    else:
        info['miuDecisionTimes'] = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]

    timeEnd = info['miuDecisionTimes'][-1] # assume last decision time is end of problem
    info['timeEnd'] = timeEnd
    tlist = np.arange(0,timeEnd+dt,dt)
    nTimeSteps = len(tlist)
    info['nTimeSteps'] = nTimeSteps
    

   #-----> number of technolologies 
    
    if 'nTechs' in kwargs.keys():
        info['nTechs'] = kwargs['nTechs']
    else:
        info['nTechs'] = 1  # Default values always aimed to get as close as possible to default DICE   
    nTechs = info['nTechs']

   #-----> allowable emissions 

    if 'freeAbateTotal' in kwargs.keys():
        info['freeAbateTotal'] = kwargs['freeAbateTotal'] # units of init emission equivalents 
    else:
        info['freeAbateTotal'] = 0.0
    state['cumFree'] = 0.0  # cumulative emissions (tCO2)

    #-----> allowable emissions 
        
    if 'carbonBudget' in kwargs.keys():
        info['carbonBudget'] = kwargs['carbonBudget']
    else:
        info['carbonBudget'] = -999.  # Negative value means unlimited budget   
          
       #-----> upper and lower bound on the sum of mius for each technology

    if 'limMiuLower' in kwargs.keys():
        if isinstance(kwargs['limMiuLower'], list):
            info['limMiuLower'] = kwargs['limMiuLower']
        else:
            info['limMiuLower'] = len(info['miuDecisionTimes'])*[kwargs['limMiuLower']]
    else:
        info['limMiuLower'] = len(info['miuDecisionTimes'])*[0]
    info['limMiuLower'] = np.array(info['limMiuLower'] , dtype = float) 

    if 'limMiuUpper' in kwargs.keys():
        if isinstance(kwargs['limMiuUpper'], list):
            info['limMiuUpper'] = kwargs['limMiuUpper']
        else:
            info['limMiuUpper'] = len(info['miuDecisionTimes'])*[kwargs['limMiuUpper']]
    else:
        info['limMiuUpper'] = len(info['miuDecisionTimes'])*[1.2]  # DICE default
    info['limMiuUpper'] = np.array(info['limMiuUpper'] , dtype = float) 

    if 'miuInitialCondition' in kwargs.keys():
        if isinstance(kwargs['miuInitialCondition'], list):
            info['miuInitialCondition'] = kwargs['miuInitialCondition']
        else:
            info['miuInitialCondition'] = len(info['miuDecisionTimes'])*[kwargs['miuInitialCondition']]
    else:
        info['miuInitialCondition'] = info['limMiuUpper'] 
    info['miuInitialCondition'] = np.array(info['miuInitialCondition'] , dtype = float) 

    # optimize on savings rate?

    if 'optSavings' in kwargs.keys():
        info['optSavings'] = kwargs['optSavings']
    else:
        info['optSavings'] = True

    #----------------------------------------------------------------------------------------------
    # tech mix decision times?

    if 'techDecisionTimes' in kwargs.keys():
        info['techDecisionTimes'] = kwargs['techDecisionTimes']
    else:
        info['techDecisionTimes'] = miuDecisionTimes    # savings rate decision times?
        
    #----------------------------------------------------------------------------------------------
    # free abatement decision times?

    if 'freeDecisionTimes' in kwargs.keys():
        info['freeDecisionTimes'] = kwargs['freeDecisionTimes']
    else:
        info['freeDecisionTimes'] = miuDecisionTimes    # savings rate decision times?
    #----------------------------------------------------------------------------------------------
    # savings rate decision times?

    if 'savingsDecisionTimes' in kwargs.keys():
        info['savingsDecisionTimes'] = kwargs['savingsDecisionTimes']
    else:
        info['savingsDecisionTimes'] = miuDecisionTimes    # savings rate decision times?
      
    if 'decisionInterpSwitch' in kwargs.keys():
        info['decisionInterpSwitch'] = kwargs['decisionInterpSwitch']
    else:
        info['decisionInterpSwitch'] = 1 # right now, default is linear interpolation


    #----------------------------------------------------------------------------------------------
    # miu decisions

    if 'miuDecisions' in kwargs.keys():
        info['miuDecisions'] = kwargs['miuDecisions']
    else:
        info['miuDecisions'] = []    # miuDecisions

    #----------------------------------------------------------------------------------------------
    # tech decisions

    if 'techDecisions' in kwargs.keys():
        info['techDecisions'] = kwargs['techDecisions']
    else:
        info['techDecisions'] = []    # tech decisions?


    #----------------------------------------------------------------------------------------------
    # savings decisions

    if 'savingsDecisions' in kwargs.keys():
        info['savingsDecisions'] = kwargs['savingsDecisions']
    else:
        info['savingsDecisions'] = []    # savings rate decision times?


    #---------------------------------------------------------------------------------------------
    #-----> techLearningCurve: Does the technology have a learning curve? 

    if 'techLearningCurve' in kwargs.keys():
        info['techLearningCurve'] = vecForm(kwargs['techLearningCurve'], nTechs)
    else:
        info['techLearningCurve'] = nTechs*[False]


     #-----> techInitCost

    if 'techInitCost' in kwargs.keys():
        info['techInitCost'] = vecForm(kwargs['techInitCost'], nTechs)
    else:
        info['techInitCost'] = nTechs*[1.] #@@@@@@@@@@ COINmode @@@@@@@@@@@@       
      
     #-----> techInitAmount

    if 'techInitAmount' in kwargs.keys():
        info['techInitAmount'] =  vecForm(kwargs['techInitAmount'], nTechs)
    else:
        info['techInitAmount'] = nTechs*[0.] # Note: techInitAmount must be specified if this technology has a learning curve.
    state['cumAbateTech'] = info['techInitAmount']  

     #-----> techLearningRate:  Improvement per year if no learning rate, else exponent on power law

    if 'techLearningRate' in kwargs.keys():
        info['techLearningRate'] = vecForm(kwargs['techLearningRate'], nTechs)
    else:
        info['techLearningRate'] = nTechs*[ 1.-(1.-0.025)**0.2] # Nominally 0.5% per year but slightly different to be more consistent with DICE
  
   #-----> firstUnitFractionalCost
 
    if 'firstUnitFractionalCost' in kwargs.keys():
        info['firstUnitFractionalCost'] = vecForm( kwargs['firstUnitFractionalCost'], nTechs)
    else:
        info['firstUnitFractionalCost'] = nTechs*[0.]  # vanilla DICE

    #-----> utilityOption
 
    if 'utilityOption' in kwargs.keys():
        info['utilityOption'] = kwargs['utilityOption']
    else:
        info['utilityOption'] = 0  # vanilla DICE       
           
    #if 'innovationRatio' in kwargs.keys() and (info['learningCurveOption'] == 4 or   info['learningCurveOption'] == 4):
    #    info['innovationRatio'] = kwargs['innovationRatio']
  
   #----->       damageCostRatio = 1.0 by default (ratio of climate damage cost to default value).
 
    if 'damageCostRatio' in kwargs.keys():
        info['damageCostRatio'] = kwargs['damageCostRatio']
    else:
        info['damageCostRatio'] = 1.0  # default to DICE default
  
   #----->       abatementCostRatio = 1.0 by default (ratio of abatement cost to default value).
 
    if 'abatementCostRatio' in kwargs.keys():
        info['abatementCostRatio'] = kwargs['abatementCostRatio']
    else:
        info['abatementCostRatio'] = 1.0  # default to DICE default
       

    #----->       gama :: elasticity of capital productivitty
 
    if 'gama' in kwargs.keys():
        info['gama'] = scalar(kwargs['gama']) # make sure it is scalar
    else:
        info['gama'] = 0.3  # default is 0.3

    #----->       depk :: depreciation rate
 
    if 'depk' in kwargs.keys():
        info['depk'] = scalar(kwargs['depk'])
    else:
        info['depk'] = 0.1  # default to 1% per year

    #----->       dela :: rate of growth of total factor productivity
 
    if 'dela' in kwargs.keys():
        info['dela'] = scalar(kwargs['dela'])
    else:
        info['dela'] = 0.01  # default to 1% per year

    # pure rate of time preference? [discount rate]

    if 'prstp' in kwargs.keys():
        info['prstp'] = scalar(kwargs['prstp']) #   Initial rate of social time preference per year   /.015  /
    else:
        info['prstp'] = 0.03

    # Minimum time between savings decisions

    if 'dtMinChoice' in kwargs.keys():
        info['dtMinChoice'] = max(dt,scalar(kwargs['dtMinChoice'])) #   Initial rate of social time preference per year   /.015  /
    else:
        info['dtMinChoice'] = 10.0

    #----->       parallel =  # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
    # number of cores to use, 0 or 1 is single core,
 
    if 'parallel' in kwargs.keys():
        info['parallel'] = kwargs['parallel']
    else:
        info['parallel'] = 1  # default to 1 core

     #-----> maximumm number of iterations 

    if 'maxeval' in kwargs.keys():
        info['maxeval'] = kwargs['maxeval']
    else:
        info['maxeval'] = 1000    
        
    #-----> SEED midaco options 

    if 'SEED' in kwargs.keys():
        info['SEED'] = kwargs['SEED']
    else:
        info['SEED'] = 0
 
    #-----> FOCUS midaco options 

    if 'FOCUS' in kwargs.keys():
        info['FOCUS'] = kwargs['FOCUS']
    else:
        info['FOCUS'] = 0

    #-----> ANTS midaco options 

    if 'ANTS' in kwargs.keys():
        info['ANTS'] = kwargs['ANTS']
    else:
        info['ANTS'] = 0

    #-----> KERNEL midaco options 

    if 'KERNEL' in kwargs.keys():
        info['KERNEL'] = kwargs['KERNEL']
    else:
        info['KERNEL'] = 0
       
    #-----> ANTS midaco options 

    if 'EVALSTOPint' in kwargs.keys():
        info['EVALSTOPint'] = kwargs['EVALSTOPint']
    else:
        info['EVALSTOPint'] = 20000. # Interval for testing evaluation stop

    #-----> KERNEL midaco options 

    if 'EVALSTOPtol' in kwargs.keys():
        info['EVALSTOPtol'] = kwargs['EVALSTOPtol']
    else:
        info['EVALSTOPtol'] = 1.e-10

    #-----> Population option 

    if 'population' in kwargs.keys():
        info['population'] = kwargs['population']
    else:
        info['population'] = 0

    if 'population_cof' in kwargs.keys():
        info['population_cof'] = kwargs['population_cof']
    else:
        info['population_cof'] = 0.005


    #---------------------------------------------------------------------------
    #------- Get various DICE parameter values ---------------------------------
    #---------------------------------------------------------------------------
    info['tlist'] = tlist
    
    state['cumEInd'] = 0.0

    prstp = info['prstp']

  
    #** capital and productivity

    gama = info['gama']
    depk = info['depk']
    dela = info['dela']

    #info['rr'] = np.exp( -prstp* tlist)
    info['rr'] = np.exp(-prstp * tlist)

    optlrsav =gama* ( depk + dela / (1- gama)) / ( depk + prstp )

    info['optlrsav'] = optlrsav


    # note in the following, it is assumed that production at 0 is equal to 1/per year, so multiplying it times something with
    # the units of time gives the unit of
    k0 = 1.0 * gama / (depk + prstp) # - 0.011 # the one is initial Y0 in units of production per year
    state['k'] =k0

    #info['al'] = ( optlrsav /depk )**-gama * np.exp( dela * tlist)
    info['al'] = k0**-gama *np.exp(dela *  tlist)

    #info['sigma'] = 1.01**-tlist # the units on sigma are relative to base case emissions
    #                              assumption is base case if sustained would warm 2 C in 100 years.
    info['sigma'] = np.exp( -0.01 * tlist )

    

    
    info['expcost2'] = 2 #  Exponent of control cost function               / 2.6  /

    info['alpha'] = 0.02 #   Assume 0.02 C warming per year initial condition emissions 
    #                        based on concept of 2 C warming in 100 years if sustained initial condition emissions

    info['a1'] = 0. #       Damage intercept                                 /0       /
    info['a2'] = 0.005 #    Fraction of GDP per degree of warming squared 2 % damages at 2 C temp increase
    info['a3'] = 2  #       Damage exponent                                  /2.00    /

    #info['K0'] = 300.e12 # USD$ capital -- not real should be tau * Y0.
    #info['Y0'] = 100.e12 # USD$/yr gross production  -- not real, Y0 = 1 by definition in base case K0 = tau
        # q0 in vanilla DICE is 105.177 trillion USD.


    info['tau'] = info['gama']  / ( info['depk'] + info['prstp'] ) #  = info['K0']/info['Y0'] # time constant relating reference state gross production 


    # -----------------------------------------------------------------
    # create dictionary for diagnostic output.
    # All items are numpy arrays with first dimension as time, and second dimension as tech if available

    timeShape = np.zeros(nTimeSteps)
    timeTechShape = np.zeros((nTimeSteps,nTechs))

    # state variables

    info['tatm'] = timeShape.copy()

    info['k'] = timeShape.copy()
    info['cumAbateTech'] = timeTechShape.copy() # not always a state variable

    # dstate variables

    info['dk'] = timeShape.copy()

    # informational

    info['yGross'] = timeShape.copy()
    info['damageFrac'] = timeShape.copy()
    info['damages'] = timeShape.copy()
    info['y'] = timeShape.copy()
    info['c'] = timeShape.copy()
    
    info['rsav'] = timeShape.copy()
    info['inv'] = timeShape.copy()

    info['periodu'] = timeShape.copy()
    info['cemutotper'] = timeShape.copy()
    
    info['eGross'] = timeShape.copy()
    info['eInd'] = timeShape.copy()
    info['abateAmount'] = timeShape.copy() 
    info['abateAmountTech']  =  timeTechShape.copy()
    info['abateFrac'] = timeShape.copy()
    
    info['abateCost'] = timeShape.copy()
    info['abateCostTech']  =  timeTechShape.copy()
    
    info['pBackTime']  =  timeTechShape.copy()  
    
    info['mcAbate'] = timeShape.copy()
    info['mcAbateTech'] = timeTechShape.copy()

    info['miu'] = timeShape.copy() 
    info['miuTech'] = timeTechShape.copy()

    info['freeAbateAmount'] = timeShape.copy() 

    if info['population'] == 0:
        info['L'] = np.ones(nTimeSteps)
    elif info['population'] == 1:
        info['L'] = timeShape.copy()
        info['L'][0] = 1
        for i in range(1, int(nTimeSteps)): 
            info['L'][i] = info['L'][0] * np.exp(info['population_cof']*i)
    elif info['population'] == 2:
        info['L'] = timeShape.copy()
        info['L'][0] = 1
        for i in range(1, int(nTimeSteps)): 
            info['L'][i] = info['L'][i-1] * (1.5/info['L'][i-1])**(20*info['population_cof'])
    
    return state,info

#%%

def vecForm(v,nTechs):
        if isinstance(v, list):
            return v
        else:
            return nTechs * [v]

#%%

def dstatedt(state, info):

    # note: state is a dictionary of scalars of current state of the system
    #       everything else is either a vector of length time, or an array of time x nTechs
    
    dstate = {}
    epsilon = 1.e-20 # small number (almost zero)
    bignum = 1.e20 # big number (almost infinity)
    
    # these three get created just because they get used alot

    idxTime = info['idxTime']
    nTechs = info['nTechs']
    firstUnitFractionalCost = info['firstUnitFractionalCost']  
    techLearningCurve =  info['techLearningCurve']

    tAtmState = info['alpha']*state['cumEInd']
     
    expcost2 = info['expcost2'] 
     

    # these get created because they get updated
    miu = info['miu']
    miuTech = info['miuTech'] # These are each technologies (including non decision technologies), summing to miu
    miuRatios = info['miuRatios']  # This is ratio of decision technologies to each other, summing to one
    yGross = info['yGross']
    eGross = info['eGross']
    pBackTime = info['pBackTime']
    mcAbate = info['mcAbate']
    mcAbateTech = info['mcAbateTech']
    abateCost = info['abateCost']
    abateCostTech = info['abateCostTech']
    abateAmount = info['abateAmount']
    abateAmountTech = info['abateAmountTech']
    abateFrac = info['abateFrac']

    damages = info['damages']
    damageFrac = info['damageFrac']

    freeAbateFract = info['freeAbateFract']
    freeAbateAmount = info['freeAbateAmount']

    rsav = info['rsav']
    inv = info['inv']

    c = info['c']
    y = info['y']

    periodu = info['periodu']
    cemutotper = info['cemutotper']

    eInd = info['eInd']


    # tendencies for recording
    k = info['k']
    dk = info['dk']
    tatm = info['tatm']
    cumAbateTech = info['cumAbateTech']




    #-------------------------------------------------------------------------------------------------
    # compute pBackTime

    for idxTech in list(range(nTechs)):
        if techLearningCurve[idxTech]:
            #Learning curve
            cumAbateTech0 = max(0.0,state['cumAbateTech'][idxTech])
            pBackTime[idxTime,idxTech] =  (
                info['abatementCostRatio'] * info['techInitCost'][idxTech]*
                (cumAbateTech0 /info['techInitAmount'][idxTech]) ** -info['techLearningRate'][idxTech]
            )
        else:
            # DICE-like representation
            pBackTime[idxTime,idxTech] = (
                info['abatementCostRatio'] * info['techInitCost'][idxTech] * 
                np.exp(-info['techLearningRate'][idxTech]*idxTime*info['dt']) 
            )

    #-------------------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------

    # Climate damage cost at t
    tAtmDamage = max(0.0, tAtmState)  # do not consider damage function for temperatures < 0.

    damageFrac[idxTime] = info['damageCostRatio'] * ( info['a1'] * tAtmDamage + info['a2'] * tAtmDamage**info['a3'] )

    # yGrossPotential =  info['al'][idxTime]  * max(state['k'],epsilon)**info['gama']

    yGrossPotential =  info['al'][idxTime] * info['L'][idxTime]**(1 - info['gama']) * max(state['k'],epsilon)**info['gama']

    damages[idxTime] =  damageFrac[idxTime] * yGrossPotential
    
    yGross[idxTime] = (1 - damageFrac[idxTime]) * yGrossPotential

    # Gross domestic product GROSS of damage and abatement costs at t ($ 2005 per year)
    # DICE:  yGross[idxTime] = yGrossPotential

    # Industrial CO2 emission at t (tCO2)
    eGross[idxTime] = yGross[idxTime] * info['sigma'][idxTime] # what industrial emissions would be in the absence of abatement

    freeAbateAmount[idxTime] = 0.
    miuFree = 0.
    if info['freeAbateTotal'] >= 0:

        remainingFree = info['freeAbateTotal'] - state['cumFree']
        freeAbateAmount[idxTime] = min(miu[idxTime] * eGross[idxTime],remainingFree * freeAbateFract[idxTime])
        # allow free abatement to only be a fraction of overall abatement

        miuFree = freeAbateAmount[idxTime] / eGross[idxTime]
    dstate['cumFree'] = freeAbateAmount[idxTime]


    miuEff = miu[idxTime] - miuFree

    if info['carbonBudget'] >= 0:

        remainingBudget = info['carbonBudget'] - state['cumEInd'] 

        if eGross[idxTime] * (1 - miuEff) > remainingBudget + freeAbateAmount[idxTime]:
            miuEff = 1.0 -  ( remainingBudget + freeAbateAmount[idxTime]) / eGross[idxTime]

    mcAbate[idxTime] = 1.e20

    for idxTech in list(range(nTechs)):
        miuTech[idxTime,idxTech] = max(0.,miuEff) * miuRatios[idxTime,idxTech] # if free abatement produces negative emissions miuEff = 0
        mcAbateTech[idxTime,idxTech] =   pBackTime[idxTime,idxTech] *(firstUnitFractionalCost[idxTech] + (1.0 - firstUnitFractionalCost[idxTech])* max(epsilon,miuTech[idxTime,idxTech])**(expcost2 - 1.0))
        mcAbate[idxTime] = min(mcAbate[idxTime],mcAbateTech[idxTime,idxTech]) 

    abateCost[idxTime] = 0.0
    for idxTech in list(range(nTechs)):
            
        abateCostTech[idxTime,idxTech] = (
            eGross[idxTime] *  pBackTime[idxTime,idxTech] * 
            ( firstUnitFractionalCost[idxTech] * miuTech[idxTime,idxTech]  + (1.0 - firstUnitFractionalCost[idxTech] ) *   max(epsilon,miuTech[idxTime,idxTech]) **expcost2 / expcost2) 
        )
        abateCost[idxTime] += abateCostTech[idxTime,idxTech]

        abateAmountTech[idxTime,idxTech] = eGross[idxTime]  * miuTech[idxTime,idxTech]
        abateAmount[idxTime] += abateAmountTech[idxTime,idxTech] 

    # this next thing is a try to get convergence (this is hocus pocus superstition)

    dstate['cumAbateTech'] = abateAmountTech[idxTime]

    eInd[idxTime] =  eGross[idxTime]  * (1 -  miuEff) - freeAbateAmount[idxTime]  # industrial emissions

    # Forest-related CO2 emissions
    # Total CO2 emission at t (tCO2)

    dstate['cumEInd'] = eInd[idxTime]


    abateFrac[idxTime] = abateCost[idxTime] / yGross[idxTime]    # <abateCost> is total of abatement this time step 

    # Gross domestic product NET of damage and abatement costs at t ($ 2005 per year)
    y[idxTime] = yGrossPotential - damages[idxTime] - abateCost[idxTime]

    # Investment at time t
    if info['optSavings']:
        rsav[idxTime] = info['savings'][idxTime] 
    else:
        rsav[idxTime] = info['optlrsav']

    # ||| adjust for case where the optizer wants to consume more than it has.
    inv[idxTime] =  max(-state['k']*(1.-info['depk']), rsav[idxTime] * y[idxTime]) 
    # negative investment means consuming capital


    # Consumption ($ 2005)
    c[idxTime] = y[idxTime] - inv[idxTime]
    consumption = max(c[idxTime],epsilon)

    if abs (info['utilityOption']  - 1.0) >  epsilon:
        # DICE utility function
        alpha = info['utilityOption']
        periodu[idxTime] = (consumption**(1- alpha) - 1.0) / (1-alpha)
    else:
        # utility = consumption
        periodu[idxTime] = consumption

    # Period utility
    #cemutotper[idxTime] = periodu[idxTime] *info['L'][idxTime]  * info['rr'][idxTime] 
    cemutotper[idxTime] = periodu[idxTime] * info['rr'][idxTime] 

    # ----------- create tendencies

       # Time rate of change of capital

    dstate['k'] = inv[idxTime] - info['depk']* state['k'] 
  
    
         
    #-------------------------------------------------------------------------

    # note only need to add things here that are not 
    # tendencies for recording
    k[idxTime] = state['k']
    dk[idxTime] = dstate['k']
    cumAbateTech[idxTime] = state['cumAbateTech']

    tatm[idxTime] = tAtmDamage
 
    return dstate

#%%
# step function interpolation

def interpStep(t, timePoints, dataPoints):
    # returns the value of the dataPoint with a time value 
    # timePoints is assumed to be sorted in ascending order
    # returns dataPoints[0] if t < timePoints[0]
    if t >= max(timePoints):
        res = dataPoints[-1]
    else:
        idx = next(ii for ii,vv in enumerate(timePoints) if vv > t)
        idx = max(0,idx-1)
        res = dataPoints[idx]
    return res

#%%

# interpolates to list with zero derivatives at data points

def safeInterpToList(xList,xData,yData, interpChoice):

    if interpChoice == 0: #step function
        fn = scipy.interpolate.interp1d(xData,yData, kind='previous')
        result = fn(xList)

    elif interpChoice == 1 or interpChoice == 2:  # linear
        result = np.interp(xList,xData,yData)

    elif interpChoice == 3:  # safe spline

        # Interpolates with all joins having a slope of zero at points that are local maxima or minima !!
        # we assume that time periods are at least dt apart
        # this one loops on xData values rather than xList values in the interest of efficiency

        fn = interpolate.PchipInterpolator(xData,yData)
        result = fn(xList)
    return result

def distribDecisions(timeList, x, dtMinChoice):
    # Assume:
    #
    # If there is a positive value in timeList, then there is one relevant decision: the y value
    # If there are two positive values in timeList, then there are two relevant decisions, the x value
    # and the y value.

    # we assume first and last values are positive and there is more than 2 x dtMinChoice spacea available for
    # each choice.

    nTimes = len(timeList)
    xReturn = x

    # make list of start and stop indices for negative runs
    # recall that the first and last values must be positive
    posToNeg = [idx for idx in range(nTimes -1) if timeList[idx]>=0 and timeList[idx+1]<0]
    negToPos = [idx for idx in range(nTimes -1) if timeList[idx]<0 and timeList[idx+1]>=0]

    for idx in range(len(posToNeg)):
        idxLastPos = posToNeg[idx]
        idxLastNeg = negToPos[idx]
        minSpace = dtMinChoice * (1+ idxLastNeg - idxLastPos)
        xList = np.append(0.,np.append(np.sort(x[idxLastPos+1:idxLastNeg+1]),1.))
        deltaX = xList[1:]- xList[:-1]
        availableSpace = timeList[idxLastNeg+1] - timeList[idxLastPos] - minSpace

        for ii in range(idxLastPos+1,idxLastNeg+1):
            iiXList = ii - (idxLastPos + 1)
            xReturn[ii] = xReturn[ii-1] + dtMinChoice + deltaX[iiXList] * availableSpace
    return xReturn

    
def scalar(a):
    if type(a) == tuple:
        return a[0]
    else:
        return a



#%%

def COIN_fun(act,state,info):
    #  This is the function called by <wrapper>, called by the midaco solver

    # It contains the actions that the solver is solving for, the initial state of the system, and general system info.
    # (Initial state of the system could also be stored in info [as a future modification].)

    # This function does two different things:

    # It takes the decision variables in a form that is convenient for the solver (i.e., lists for real decisions only), and converts it
    # into a form that is convenient for the differential equations (i.e., lists by time steps)

    # The steps of this function are:

    # 1. Expand <act> for decisions to decision times made implicit by constraints or specification.

    # 2. Interpolate decision times to time steps.
    # #     (This was brought outside the time loop, because repeated interpolation was causing things to run slowly.)

    # 3. Time step through differential equations.


    # Initially we are going to assume that the only decision are the abatement
    # level MIU.
    # relies on globals <state> and <info>

    # The action vector is defined as follows:

    # Action vector <act>
    #   # OF ELEMENTS           VALUE
    #   nMiuLevelDecisions      Choices for selectable miu values
    #   nMiuTimeDecisions       Choices for selectable miu decision times
    #   (nTechs - 1)*nMiuTechDecisions
    #                           Choices for miuTech values
    #   nMiuTechTimeDecisions   Choices for selectable miuTech decision time values
    #   nSavingLevelDecisions   Choices for rsav values
    #   nsavingsDecisionTimes    Choices for rsav times 

    tlist = info['tlist']
    dt = info['dt']
    nTimeSteps = info['nTimeSteps']



    # ------------------------------------------------------------------------
    # 1. unpack act
    # ------------------------------------------------------------------------

    # First unpack time elements in the order: miu, miuTech, savings, free abatement (if present)

    # now do x values (time periods or choices about time periods if decisionTime is negative)

    # miu

    miuDecisionTimes = info['miuDecisionTimes']
    nMiuTimes = len(miuDecisionTimes)

    idxAct = 0 
    xx = np.zeros(nMiuTimes)
    for idx in range(nMiuTimes):
        if miuDecisionTimes[idx] >= 0:
            xx[idx] = miuDecisionTimes[idx]  # time choice
        else: # Time is to be determined: value is choice
            xx[idx] = act[idxAct]
            idxAct += 1

    xMiu = distribDecisions(miuDecisionTimes, xx, info['dtMinChoice']) # convert to a string of time values

    info['xMiu'] = xMiu

    # miuTech
     
    techDecisionTimes = info['techDecisionTimes']
    nTechTimes = len(techDecisionTimes) 
    x = np.zeros(nTechTimes)
    for idx in range(nTechTimes):
        if techDecisionTimes[idx] >= 0:
            x[idx] = techDecisionTimes[idx]  # time choice
        else: # Time is to be determined: value is choice
            x[idx] = act[idxAct]
            idxAct += 1

    xTech = distribDecisions(techDecisionTimes, x, info['dtMinChoice']) # convert to a string of time values

    info['xTech'] = xTech

    # savings
    xS = []
    if info['optSavings'] == True:
        savingsDecisionTimes = info['savingsDecisionTimes']
        nSavingsTimes = len(savingsDecisionTimes) 
        xS = np.zeros(nSavingsTimes)
        for idx in range(nSavingsTimes):
            if savingsDecisionTimes[idx] >= 0:
                xS[idx] = savingsDecisionTimes[idx]  # time choice
            else: # Time is to be determined: value is choice
                xS[idx] = act[idxAct]
                idxAct += 1
    
        xSavings = distribDecisions(savingsDecisionTimes, xS, info['dtMinChoice']) # convert to a string of time values
        info['xSavings'] = xSavings


    # free abatement decisions
    xF = []
    if info['freeAbateTotal'] > 0:

        freeDecisionTimes = info['freeDecisionTimes']
        nFreeDecisionTimes = len(freeDecisionTimes) 
        xF = np.zeros(nFreeDecisionTimes)
        for idx in range(nFreeDecisionTimes):
            if freeDecisionTimes[idx] >= 0:
                xF[idx] = savingsDecisionTimes[idx]  # time choice
            else: # Time is to be determined: value is choice
                xF[idx] = act[idxAct]
                idxAct += 1
    
        xFree = distribDecisions(freeDecisionTimes, xF, info['dtMinChoice']) # convert to a string of time values
        info['xFree'] = xFree
 
    #======================================================
    #======================================================
    #======================================================
    # -----> initialize miu decisions


    limMiuUpper = info['limMiuUpper']
    limMiuLower = info['limMiuLower']

    nMiuLevelDecisions = np.count_nonzero(limMiuUpper - limMiuLower)  # This expression counts the number of different values
    nMiuLevels = len(miuDecisionTimes)

    yMiu = np.zeros(nMiuLevels)

    for idx in range(nMiuLevels):
        if limMiuUpper[idx] == limMiuLower[idx]:
            yMiu[idx] = limMiuUpper[idx]
        else:
            yMiu[idx] = act[idxAct]
            idxAct += 1

    info['yMiu'] = yMiu

   #======================================================
    # -----> initialize miuRatio decisions (tech)

    techDecisionTimes = info['techDecisionTimes']
    nTechs = info['nTechs']
    nTechTimes = len(techDecisionTimes)

    techDecisionArray = np.reshape(
        act[ idxAct : idxAct + nTechTimes * (nTechs-1) ],(nTechs-1,nTechTimes)
        ) 
    idxAct = idxAct + (nTechs-1)*nTechTimes

    yTechArray = -np.ones(((nTechTimes,nTechs)))
    remaining = np.ones(nTechTimes)
    idxTechDecision = 0
    for idxTech in list(range(nTechs)):
        if idxTechDecision < len(techDecisionArray):
            yTechArray[:,idxTech] = remaining * techDecisionArray[idxTechDecision]
            remaining = remaining * (1.0 - techDecisionArray[idxTechDecision])
            idxTechDecision += 1
        else: # last one gets remaining
            yTechArray[:,idxTech] = remaining
    info['yTechArray'] = np.ravel(np.transpose(yTechArray))

    #======================================================
    # -----> initialize savings decisions

    if info['optSavings']:
        
        ySavings = act[idxAct:idxAct + nSavingsTimes]
        idxAct = idxAct + nSavingsTimes
    else: # specified savings
        ySavings = np.array([info['optlrsav'] for item in info['savingsDecisionTimes']])
    info['ySavings'] = ySavings

    # -----> initialize free abatement decisions

    if info['freeAbateTotal'] > 0.:   
        yFree = act[idxAct:idxAct + nFreeDecisionTimes]
        idxAct = idxAct + nFreeDecisionTimes
        info['yFree'] = yFree   

    # ------------------------------------------------------------------------
    # 2. now interpolate across time steps
    # ------------------------------------------------------------------------   

    #  for miuratios, change from cumulative to actual ratios.
    #  i.e., on input if miu  = 0.8, and miuRatio = [0.25, 0.333333, 0.5]
    # we would have on cumulative (0.25 x 0.8) = 0.2; 0.8 - 0.2 = 0.6; (0.3333 * 0.6 ) = 0.2; ... 
    # or in terms of 
    # This would be converted to, miu = 0.8 and miuRatios = [0.25, 0.25, 0.25, 0.25]

    miu = safeInterpToList(tlist,xMiu,yMiu,info['decisionInterpSwitch'])
    info['miu'] = miu 

    miuRatios = np.zeros((nTimeSteps,nTechs))

    for idxTech in list(range(nTechs)):
        miuRatios[:,idxTech] = safeInterpToList(tlist,xTech,yTechArray[:,idxTech],info['decisionInterpSwitch'])
    info['miuRatios'] = miuRatios

    if (len(xSavings)!= len(ySavings)):
        print ('Savings problem ',len(xSavings),len(ySavings))
    savings = safeInterpToList(tlist,xSavings,ySavings,info['decisionInterpSwitch'])

    info['savings'] = savings 

    if info['freeAbateTotal'] > 0.:
        if (len(xFree)!= len(yFree)):
            print ('Free problem ',len(xFree),len(yFree))
        if info['decisionInterpSwitch'] == 2:
            savingsInterp = 3
        else:
            savingsInterp = info['decisionInterpSwitch']
        freeAbateFract = safeInterpToList(tlist,xFree,yFree,savingsInterp)

        info['freeAbateFract'] = freeAbateFract
    else:
        info['freeAbateFract'] = np.zeros(len(tlist))

     # ------------------------------------------------------------------------
    # 3. now time step the action
    # ------------------------------------------------------------------------  

    for idxTime in list(range(info['nTimeSteps'])):
        info['idxTime'] = idxTime
         
        dstate = dstatedt(state, info)  # info is a global used by dstatedt
        
        # eulers method (1 is OK, 0.5 seems fine)
        for key in state:
            state[key] +=  dt * dstate[key]

    #obj = dt*np.sum(info['cemutotper'])+((state['k']-dt*dstate['k'])*(1+info['prstp'])**(-nTimeSteps*dt)-1)/info['tau']
    obj = dt*np.sum(info['cemutotper'])
    info['npvUtility'] = obj

    return float(obj),info

#############################################################################
#####    Main DICE Function                              ####################
#####    Class is used to transfer data among functions  ####################
#############################################################################

class COIN_instance:

    def __init__(self, **kwargs):

        state, info = initStateInfo(kwargs)

        self.state = state
        self.info = info
        self.out = self.runDICEeq() 
    
    def wrapper(self, act):

        state = self.state
        info = self.info
        welfare, info = COIN_fun(act,state,info)

        # "Without loss of generality, all objectives are subject to minimization."
        # http://www.midaco-solver.com/data/other/MIDACO_User_Manual.pdf

        ret = -welfare

        return [[ret],[0.0]]

    def runDICEeq(self):

        state = self.state
        info = self.info
        
        # There are three types of actions:

        # miu[reducedDecisionTimeSteps] -- actions to decide on overall abatement level (miu)
        
        # miuRatio[idx, decisionTimeSteps] (for idx all but last technology with a decision)

        # savings rate

        # ====================
        #  First time dimensions

        random.seed(info['SEED']) # set random number generator

        # Prepare miu decisions
        miuDecisionTimes = info['miuDecisionTimes']
        # negative means find both time and value
        nMiuTImes = len(miuDecisionTimes)
        nMiuTimeDecisions = len([num for num in miuDecisionTimes if num < 0])

        xMiuTime = [-num*random.random() for num in miuDecisionTimes if num < 0]
        xMiuTimeUpper = np.ones(nMiuTimeDecisions)
        xMiuTimeLower = np.zeros(nMiuTimeDecisions)

        # Prepare tech decisions
        techDecisionTimes = info['techDecisionTimes']
        # negative means find both time and value
        nTechDecisions = len(techDecisionTimes)
        nTechTimeDecisions = len([num for num in techDecisionTimes if num < 0])

        xTechTime = [-num*random.random() for num in techDecisionTimes if num < 0]
        xTechTimeUpper = np.ones(nTechTimeDecisions)
        xTechTimeLower = np.zeros(nTechTimeDecisions)

        # Prepare use of free carbon budget decisions

        xFreeDecisionTimes = []
        xFreeDecisionTimesUpper = []
        xFreeDecisionTimesLower = []
        if info['freeAbateTotal'] > 0.: # check if there is free stuff to be 
            freeDecisionTimes = info['freeDecisionTimes']
            # negative means find both time and value
            nFreeDecisions = len(freeDecisionTimes)
            nFreeTimeDecisions = len([num for num in freeDecisionTimes if num < 0])

            xFreeDecisionTimes = [-num*random.random() for num in freeDecisionTimes if num < 0]
            xFreeDecisionTimesUpper = np.ones(nFreeTimeDecisions)
            xFreeDecisionTimesLower = np.zeros(nFreeTimeDecisions)

        if info['optSavings']:
            # Prepare miu decisions
            savingsDecisionTimes = info['savingsDecisionTimes']
            # negative means find both time and value
            nSavingsTimeDecisions = len([num for num in savingsDecisionTimes if num < 0])

            xSavingsTime = [-num*random.random() for num in savingsDecisionTimes if num < 0]
            xSavingsTimeUpper = np.ones(nSavingsTimeDecisions)
            xSavingsTimeLower = np.zeros(nSavingsTimeDecisions)
        else:
            xSavingsTime = []
            xSavingsTimeUpper = []
            xSavingsTimeLower = []
        
        # NOW DO LEVEL DECISIONS: miu, tech, free abatement, savings

        # miu decisions
        
        limMiuUpper = info['limMiuUpper']
        limMiuLower = info['limMiuLower']

        if len(info['miuDecisions']) == 0:
            nMiuLevelDecisions = np.count_nonzero(limMiuUpper - limMiuLower) # This expression counts the number of different values
        else:
            nMiuLevelDecisions = 0

        yMiu = np.ones(nMiuLevelDecisions) # start off assuming complete abatement (!!!!!This would not work if max is not 1 !!!!!!)
        yMiuLower = np.zeros(nMiuLevelDecisions) # create empty vector        
        yMiuUpper = np.zeros(nMiuLevelDecisions) # create empty vector        
        icount = 0
        for idx in range(len(limMiuUpper)):
            if limMiuUpper[idx] > limMiuLower[idx]:
                yMiuLower[icount] = limMiuLower[idx]
                yMiuUpper[icount] = limMiuUpper[idx]
                yMiu[icount] = yMiuUpper[icount] 
                #                            start by guessing exponential to 1 with 30-yr efolding
                icount += 1

        # -----> initialize miuRatio decisions

        nTechs = info['nTechs']
    
        yTechArray = np.zeros((nTechDecisions,nTechs-1))/nTechs # start at zero except first  
        if nTechs > 1:
            yTechArray[:,0] = 0.5    
        yTechLowerArray = np.zeros((nTechDecisions,nTechs-1)) # create array of zeros        
        yTechUpperArray = np.ones((nTechDecisions,nTechs-1)) # create array of ones

        # free abatement decisions

        if info['freeAbateTotal'] > 0.:  
            nFreeDecisions = len(freeDecisionTimes)
        else:
            nFreeDecisions = 0


        yFree = 0.01 * np.ones(nFreeDecisions) # start off assuming complete 1% per year abatement (!!!!!This would not work if max is not 1 !!!!!!)
        yFreeLower = np.zeros(nFreeDecisions) # create empty vector        
        yFreeUpper = np.ones(nFreeDecisions) # create empty vector         

        # -----> initialize savings decisions

        savingsDecisionTimes = info['savingsDecisionTimes']
        nSavingsRateDecisions = len(savingsDecisionTimes)
        # negatives mean find both time and value

        nTechs =  info['nTechs'] # total number of technologies in resuls

        if info['optSavings']:

            ySavingsUpper = np.ones( nSavingsRateDecisions )
            #ySavingsLower = np.zeros(nSavingsRateDecisions)
            ySavingsLower =  np.zeros( nSavingsRateDecisions )
            ySavings = np.array([info['optlrsav'] for i in range(nSavingsRateDecisions)])
            
            ySavingsLower[-1] = -10.0
            ySavings[-1] = -5.0 # assume last time period is zero as starting for optimizer
            
        else: # no savings
            ySavingsUpper = np.zeros(0)
            ySavingsLower = np.zeros(0)
            ySavings = np.zeros(0)

        # ----> put together actions

        act = np.concatenate((
            xMiuTime,xTechTime,           xSavingsTime, xFreeDecisionTimes,
            yMiu,    np.ravel(yTechArray),ySavings, yFree
            ))
        actLower = np.concatenate((
            xMiuTimeLower,xTechTimeLower,           xSavingsTimeLower,xFreeDecisionTimesLower,
            yMiuLower,    np.ravel(yTechLowerArray),ySavingsLower,yFreeLower
            ))
        actUpper = np.concatenate((
            xMiuTimeUpper,xTechTimeUpper,           xSavingsTimeUpper,xFreeDecisionTimesUpper,
            yMiuUpper,    np.ravel(yTechUpperArray),ySavingsUpper,yFreeUpper
            ))

        ########################################################################
        ### Step 1: Problem definition     #####################################
        ########################################################################

        # Note that in this version, for computational reasons, the variables used for optimization differ 
        # from those used internally by the differential equation code.

        # In the code it makes sense to have miu[idxTech] for each tech. But numerically, it is better to have the sum of all miu's as the first variable
        # and then the fraction of the sum of miu's used by the first, second, nth technology.
        # the last technology with a decision gets the remainder.

        ########################################################################
        ### Step 1: Problem definition     #####################################
        ########################################################################

        problem = {} # Initialize dictionary containing problem specifications
        option  = {} # Initialize dictionary containing MIDACO options
    
        problem['@'] = self.wrapper # Handle for problem function name
    

        # STEP 1.B: Lower and upper bounds 'xl' & 'xu'
        #############################################
        #    # STEP 1.C: Starting point 'x'
        ##############################

    
        problem['x'] = list(act)  # initial guess for control variable, convert to list

        #actupper[30:] = [info['limmiu']] * (nDecisions-30)
    
        problem['xl'] = list(actLower) # initial guess for control variable, convert to list
        problem['xu'] = list(actUpper) # initial guess for control variable, convert to list
    
        # STEP 1.A: Problem dimensions
        ##############################
        problem['o']  = 1                       # Number of objectives 
        problem['n']  = len(act) # Number of variables (in total)
        problem['ni'] = 0                       # Number of integer variables (0 <= ni <= n) 
        problem['m']  = 0      # Number of constraints (in total)  [max and min on miu for each time step]
        problem['me'] = 0                       # Number of equality constraints (0 <= me <= m)
        
        ########################################################################
        ### Step 2: Choose stopping criteria and printing options    ###########
        ########################################################################
    
        # STEP 2.A: Stopping criteria 
        #############################
        #option['maxeval'] = 100000   # Maximum number of function evaluation (e.g. 1000000) 
        option['maxeval'] = info['maxeval']   # Maximum number of function evaluation (e.g. 1000000) 
        #option['maxeval'] = 1    # Maximum number of function evaluation TEST
        option['maxtime'] = 60*60*24 # Maximum time limit in seconds (e.g. 1 Day = 60*60*24) 
    
        # STEP 2.B: Printing options  
        ############################ 
        option['printeval'] = 10000   # Print-Frequency for current best solution (e.g. 1000) 
        option['save2file'] = 1     # Save SCREEN and SOLUTION to TXT-files [0=NO/1=YES]

        ########################################################################
        ### Step 3: Choose MIDACO parameters (FOR ADVANCED USERS)    ###########
        ########################################################################
    
        option['param1']  = 0       # ACCURACY  (only affects constrained problems)
        option['param2']  = info['SEED']       # SEED (integer)
        option['param3']  = 0       # FSTOP (integer)
        option['param4']  = 0     # ALGOSTOP (integer) 
        option['param5']  = info['EVALSTOPint'] + info['EVALSTOPtol'] # EVALSTOP  
        option['param6']  = info['FOCUS']     # FOCUS  
        option['param7']  = info['ANTS']    # ANTS  
        option['param8']  = info['KERNEL']      # KERNEL -- default zero  
        option['param9']  = 0.0     # ORACLE  
        option['param10'] = 0.0     # PARETOMAX
        option['param11'] = 0.0     # EPSILON  
        option['param12'] = 0.0     # BALANCE
        option['param13'] = 0.0     # CHARACTER
    
        ########################################################################
        ### Step 4: Choose Parallelization Factor   ############################
        ########################################################################
    
        #option['parallel'] = 1 # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
        option['parallel'] = info['parallel'] # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
    
        ########################################################################
        ############################ Run MIDACO ################################
        ########################################################################
   
        startdate = datetime.datetime.now()
        print(startdate.strftime("%d/%m/%Y %H:%M:%S"))
    
        info["saveOutput"] = False
    
        # if os.getlogin()=='kcaldeira':
        #     MIDACO_KEY = b'Ken_Caldeira_(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        # elif os.getlogin()=='CandiseHenry':
        #     MIDACO_KEY = b'Candise_Henry(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        # else:
        MIDACO_KEY = b'Lei_Duan_____(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        
        solution = midaco.run( problem, option, MIDACO_KEY )
        print(solution['x'])
    
        enddate = datetime.datetime.now()
        print(enddate.strftime("%d/%m/%Y %H:%M:%S"))
        minutes_diff = (enddate - startdate).total_seconds() / 60.0
        print ('elapsed time = ',str(minutes_diff),' minutes')
    
        todayString = str(enddate.year) + str(enddate.month).zfill(2) + str(enddate.day).zfill(2) + '_' + \
        str(enddate.hour).zfill(2) + str(enddate.minute).zfill(2) + str(enddate.second).zfill(2)

        info["saveOutput"] = True
    
        utility,info = COIN_fun(solution['x'],state,info)

        info['utility'] = utility
        print(utility)
        root_dir = "."

        return [problem,option,solution,info]

# 
# %%

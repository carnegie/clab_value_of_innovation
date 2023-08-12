# -*- coding: utf-8 -*-

"""

Created on Sun Jul 12 14:53:40 2020

@author: kcaldeira

"""

from plot_utilities import *

from io_utilities import *

from COIN_diffeqs import COIN_instance


#%%

# starting point has learning curve of 10 k$ at 10,000 tCO2, and a learning rate of 12% per doubling.

if __name__ == "__main__":

    #>>>>>>>>>> Default section  >>>>>>>>>>>>

    shiftOpt = 'shift'
    maxEval = 1000000
    cores = 2 # Change this based on your machine
    initCostRef = 1.0                                                   
    rateOpt = 0.13750352374993496
    initAmounts = [1e-6]
    dt0 = 1.0
    prstpVal = 0.03, # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
    depkVal = 0.1, # depreciation is 10%/yr
    delaVal = 0.01, # no growth in total factor productivity
    gamaVal = 0.3, # elasticity of productivity
    interpSwitch = 3
    dtMinChoiceVal = 10.
    sdt = [0,dt0,-0.1,-0.1,-0.1,300-dt0,300]

    #>>>>>>>>>> Modification section  >>>>>>>>>>>>

    seedValStart = 3008 
    nSeedVals = 10 

    # ==================== Base case + cost reduction case

    rampOpts = ['balancing','budgeting','budgeting_s']
    prefix = "COIN_020_central"
    initCostList = np.insert(np.round(10.**-np.arange(0,2.05,0.05),6),0,10)
    freeAbateVals = [0.] 
    pop_opt = [0]
    initCost_1stTech = 0.2



    ##### Case summary starts here

    # ==================== Value of CO2 

    rampOpts = ['balancing','budgeting','budgeting_s']
    prefix = "COIN_020_valueOfCO2"
    initCostList = [1.]
    freeAbateVals = [10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,120.,140.,160.,180.,200.]
    pop_opt = [0]
    initCost_1stTech = 0.2

    # ==================== Pop growth case 

    rampOpts = ['balancing','budgeting','budgeting_s']
    prefix = "COIN_020_central"
    initCostList = [1.]
    freeAbateVals = [0.] 
    pop_opt = [1, 2]
    initCost_1stTech = 0.2

    # ==================== No abatement case

    rampOpts = ['no_abate']
    prefix = "COIN_020_no-abate"
    initCostList = [1.]
    freeAbateVals = [0.] 
    pop_opt = [0, 1, 2]
    initCost_1stTech = 0.2

    # ==================== No cost case
    
    rampOpts = ['balancing','budgeting','budgeting_s']
    prefix = "COIN_020_no-cost"
    initCostList = [1.]
    freeAbateVals = [0.] 
    pop_opt = [0, 1, 2]
    initCost_1stTech = 0.0

    ##### Case summary ends here



    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 

    #===== seedVal loop

    for seedVal in range(seedValStart,seedValStart + nSeedVals):

        #--------- main 0 and 10 ----------------------------------------
        for freeAbateVal in freeAbateVals:

            for initCost in initCostList:

                for rampOpt in rampOpts:
                    cBudget = -999 # flag for unlimited
                    decTimes = sdt

                    if rampOpt == 'ramping':
                        # allow for savings rate discontinuity at 30 in ramp case
                        # assumes years 0, 1, 5, 10, 15, 20 ,25, 39
                        decTimes = [0.,0.5,1.,29.,29.5,30.,30.5,300.]
                        limLower = [0.,0.5/30.,1./30.,29./30,29.5/30.,30./30.,1.,1.]
                        limUpper = limLower

                    elif rampOpt == 'max':
                        limLower = 1.0
                        limUpper = limLower
                    elif rampOpt == 'budgeting':
                        limLower = 0.0
                        limUpper = 1.0
                        cBudget = 50.
                    elif rampOpt == 'budgeting_s':
                        limLower = 0.0
                        limUpper = 1.0
                        cBudget = 15.
                    elif rampOpt == 'balancing':
                        limLower = 0.0
                        limUpper = 1.0
                    elif rampOpt == 'no_abate':
                        limLower = 0.0
                        limUpper = 0.0

                    for initAmt in initAmounts:

                        if shiftOpt == 'shift':
                            initAmount = initAmt
                        else:
                            if initCost > 0:
                                initAmount = initAmt*(initCost/initCostRef)**(-1./rateOpt)
                            else:
                                initAmount = 1.e80

                        for pop in pop_opt:

                            caseName = (prefix + '_p-' + str(pop)
                                        + '_c-' + rampOpt 
                                        + '_i-' + str(initCost)
                                        + '_f-' + str(freeAbateVal)
                                        + '_s-' + str(seedVal)
                                        + '_m-' + str(maxEval)
                                        )

                            # If no arg is given, run vanilla DICE

                            print()
                            print("=============================================================")
                            print (caseName)

                            resultCentral = COIN_instance(

                                COINmode = True, # simple version
                                
                                dt = dt0, # dt time step for integration

                                nTechs = 2, # number of technologies considered

                                decisionInterpSwitch = interpSwitch, # 0 = step function, 1 = linear, 2 = safe spline savings only, 3= safe spline

                                miuDecisionTimes = decTimes, # times for miu decisions
                                techDecisionTimes = sdt, # times for tech mix decisions
                                savingsDecisionTimes = sdt, # times for miu decisions

                                freeDecisionTimes = sdt, # times for using free abatement
                                freeAbateTotal = freeAbateVal, # Number of years worth of free abatement (for free abatement cases)

                                carbonBudget = cBudget, # number of years worth of unabated carbon (for carbon budgeting cases)

                                #limMiuLower = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # lower limit on miu values (= sum across all techs)
                                limMiuLower = limLower,
                                #limMiuLower = [0.,0.,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,
                                #                        1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],
                                #limMiuLower = 0, # can be scalar or vector of len(decisionTimes)
                                limMiuUpper = limUpper, # upper limit on miu values (= sum across all techs)
                                #limMiuUpper = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2], # upper limit on miu values (= sum across all techs)
                                #limMiuUpper = 1.0, # can be scalar or vector of len(decisionTimes)

                                optSavings = True, # True means to optimize on savings rate, False means to use default value (different for COINmode)

                                techLearningCurve = [False,True], # does this technology have a learning curve (True) or a specified cost function (False)
                                # NOTE: <learningCurveTech> must have a length of <nTechs>

                                techInitCost = [initCost_1stTech,initCost], # Initial cost for learning curve. Must be same shape as nTechs.
                                #techInitCost = [550, 1e4], # Initial cost for learning curve. Must be same shape as nTechs.
                                                                    # If no learning curve, then this value is the initial backstop cost (pback)

                                techInitAmount = [0,initAmount], # Initial cost for learning curve. Must be same shape as nTechs, but value if no learning curve is unimportant 

                                techLearningRate = [0.005,rateOpt], # 10% per doubling (1 + 0.10)**-1. Must be same shape as nTechs.
                                #techLearningRate = [0.005050763379468082, 0.23446525363702297], # 15% per doubling. Must be same shape as nTechs.
                                # techLearningRate = [0.005050763379468082, 0.18442457113742744], # 12% per doubling. Must be same shape as nTechs.
                                                                    # If no learning curve, then value is fractional cost improvement per year

                                firstUnitFractionalCost = [0.0,0.5], # Marginal cost at miuX = 0 compared to marginal cost at miuX = 1.

                                utilityOption = 1, # utilityOption == 0 --> DICE utility function; 1 --> assume consumption == utility

                                prstp = prstpVal, # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                                depk = depkVal, # depreciation is 10%/yr
                                dela = delaVal, # no growth in total factor productivity
                                gama = gamaVal, # elasticity of productivity
                                    
                                dtMinChoice = dtMinChoiceVal, # minimum time between savings decisions
                                SEED= seedVal,

                                parallel = cores, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                                maxeval = maxEval,  # maxeval maximum number of iterations for solver
                                FOCUS  = 100, # FOCUS parameter for midaco solver
                                ANTS = 81,
                                KERNEL = 27,

                                damageCostRatio = 1.0, # scaling on climate damage
                                abatementCostRatio = 1.0, # scaling on abatement costs (multiplies costs above for all techs)
                                
                                population = pop,
                                population_cof = 0.005

                            )
                            
                    pickle_results('../COIN_results/output230314',caseName,filter_dic(resultCentral.out))

                    write_CSV_from_pickle('../COIN_results/output230314',caseName)

# %%

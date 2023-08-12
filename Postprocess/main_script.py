"""

Main script

Created by Lei Duan on Nov 2, 2021

"""


import numpy as np
import csv
import matplotlib.pyplot as plt

from helper import get_f_name_list
from helper import get_csv_content
from helper import get_var_from_table
from helper import learning_subsidy


if  __name__ ==  "__main__":

    csv_ken_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Lei/Ken et al. 2021_Ken_COIN/Model and Raw Figures/COIN_018_best_csv/' 
    csv_ken_free = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Lei/Ken et al. 2021_Ken_COIN/Model and Raw Figures/best-freeAbate/' 
    csv_lei_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Lei/Ken et al. 2021_Ken_COIN/Model and Raw Figures/COIN_020_new/'

    #### Get collection names
    f_name_categories = get_f_name_list(csv_ken_path, csv_ken_free, csv_lei_path)



    """ Figure 2 and related
    # ------------------------------------------------------------------------------------------------------------------------------
    var_to_get = ['tlist', 'eInd', 'tatm', 'abateCost', 'damages', 'c']
    # var_to_get = ['c', 'mcAbate', 'abateCostTech_0', 'abateCostTech_1', 'tlist', 'miu', 'inv', 'rsav']

    # ################################# Fig2:
    var_name = 'eInd'; x1=0; x2=150; y1=0; y2=70; scale=40; name='eInd_GtCO2'; type='absolute'; fu=0
    # var_name = 'tatm'; x1=0; x2=150; y1=0; y2=4; scale=1; name='tatm_K'; type='absolute'; fu=0
    # var_name = 'abateCost'; x1=0; x2=150; y1=0; y2=11; scale=100; name='abatement_cost_T$'; type='absolute'; fu=0
    # var_name = 'c'; x1=0; x2=150; y1=0; y2=40; scale=-100; name='consumption_T$'; type='diff'; fu=0
    # ################################# FigS2, S3, S4, S5
    # var_name = ['abateCostTech_0', 'abateCostTech_1']; x1=0; x2=150; y1=0; y2=10; scale=100; name='abatement_cost_separate_T$'; type='multi'; fu=0
    # var_name = 'mcAbate'; x1=0; x2=150; y1=0; y2=450; scale=2500; name='miu_T$'; type='absolute'; fu=0
    # var_name = 'rsav'; x1=0; x2=150; y1=24; y2=27; scale=100; name='saving_rate_%'; type='absolute'; fu=1
    # var_name = 'c'; x1=0; x2=150; y1=-30; y2=2; scale=100; name='consumption_T$'; type='diff'; fu=1
    # var_name = 'inv'; x1=0; x2=150; y1=-30; y2=2; scale=100; name='inv_T$'; type='diff'; fu=1
    # var_name = 'c'; x1=0; x2=150; y1=-15; y2=60; scale=100; name='consumption_T$'; type='diff2'; fu=1
    # var_name = 'inv'; x1=0; x2=150; y1=-15; y2=60; scale=100; name='inv_T$'; type='diff2'; fu=1

    table_NoAbat, ip_NoAbat      =  get_csv_content(f_name_categories['no_abate_p0']);                        results_NoAbat    =  get_var_from_table(table_NoAbat, var_to_get, ip_NoAbat)
    table_FreeBala, ip_FreeBala  =  get_csv_content(f_name_categories['no_cost_balancing_p0']);               results_FreeBala  =  get_var_from_table(table_FreeBala, var_to_get, ip_FreeBala)
    table_FreeBudg, ip_FreeBudg  =  get_csv_content(f_name_categories['no_cost_budgeting_p0']);               results_FreeBudg  =  get_var_from_table(table_FreeBudg, var_to_get, ip_FreeBudg)
    table_FreeRamp, ip_FreeRamp  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p0']);             results_FreeRamp  =  get_var_from_table(table_FreeRamp, var_to_get, ip_FreeRamp)
    table_1tecBala, ip_1tecBala  =  get_csv_content(f_name_categories['cost_reduction_balancing'][-1]);       results_1tecBala  =  get_var_from_table(table_1tecBala, var_to_get, ip_1tecBala)
    table_1tecBudg, ip_1tecBudg  =  get_csv_content(f_name_categories['cost_reduction_budgeting'][-1]);       results_1tecBudg  =  get_var_from_table(table_1tecBudg, var_to_get, ip_1tecBudg)
    table_1tecRamp, ip_1tecRamp  =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][-1]);     results_1tecRamp  =  get_var_from_table(table_1tecRamp, var_to_get, ip_1tecRamp)
    table_2tecBala, ip_2tecBala  =  get_csv_content(f_name_categories['central_balancing_p0']);               results_2tecBala  =  get_var_from_table(table_2tecBala, var_to_get, ip_2tecBala)
    table_2tecBudg, ip_2tecBudg  =  get_csv_content(f_name_categories['central_budgeting_p0']);               results_2tecBudg  =  get_var_from_table(table_2tecBudg, var_to_get, ip_2tecBudg)
    table_2tecRamp, ip_2tecRamp  =  get_csv_content(f_name_categories['central_budgeting_s_p0']);             results_2tecRamp  =  get_var_from_table(table_2tecRamp, var_to_get, ip_2tecRamp)


    # ################################# Text here:
    # framing = 2
    # if framing == 0:
    #     eInd_2tech = results_2tecBala
    #     eInd_1tech = results_1tecBala
    # if framing == 1:
    #     eInd_2tech = results_2tecBudg
    #     eInd_1tech = results_1tecBudg
    # if framing == 2:
    #     eInd_2tech = results_2tecRamp
    #     eInd_1tech = results_1tecRamp
    # print ()
    # print () 
    # tlist = results_NoAbat['tlist']
    # eInd_2tecBala = eInd_2tech['eInd'] * 10/12*44
    # eInd_1tecBala = eInd_1tech['eInd'] * 10/12*44
    # diff_eInd = eInd_1tecBala - eInd_2tecBala
    # diff_eInd_percentage = (eInd_1tecBala - eInd_2tecBala) / eInd_1tecBala * 100
    # tatm_2tecBala = eInd_2tech['tatm'] 
    # tatm_1tecBala = eInd_1tech['tatm'] 
    # diff_tatm = tatm_1tecBala - tatm_2tecBala
    # for i in range(len(tlist)):
    #     int_eInd_2tecbala = np.sum(eInd_2tecBala[:i])
    #     int_eInd_1tecbala = np.sum(eInd_1tecBala[:i])
    #     diff_int_eInd_percentage = (int_eInd_1tecbala - int_eInd_2tecbala) / int_eInd_1tecbala * 100
    #     print (tlist[i], eInd_1tecBala[i], eInd_2tecBala[i], diff_int_eInd_percentage, diff_eInd_percentage[i] )
    #     # stop 
    # stop 
    


    tlist = results_NoAbat['tlist']
    if type == 'multi':
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
        ax1.plot(tlist, results_1tecBala[var_name[0]]*scale, color='royalblue', linestyle='--')
        ax1.plot(tlist, results_1tecBudg[var_name[0]]*scale, color='darkgreen', linestyle='--')
        ax1.plot(tlist, results_1tecRamp[var_name[0]]*scale, color='firebrick', linestyle='--')
        ax2.plot(tlist, results_2tecBala[var_name[0]]*scale, color='royalblue', linestyle='--')
        ax2.plot(tlist, results_2tecBudg[var_name[0]]*scale, color='darkgreen', linestyle='--')
        ax2.plot(tlist, results_2tecRamp[var_name[0]]*scale, color='firebrick', linestyle='--')
        ax2.plot(tlist, results_2tecBala[var_name[1]]*scale, color='royalblue', linestyle='solid')
        ax2.plot(tlist, results_2tecBudg[var_name[1]]*scale, color='darkgreen', linestyle='solid')
        ax2.plot(tlist, results_2tecRamp[var_name[1]]*scale, color='firebrick', linestyle='solid')
    else:
        ax1 = plt.subplot(111)
        if type == 'absolute':
            ax1.plot(tlist[fu:], (results_NoAbat[var_name]*scale)[fu:], color='grey')
            ax1.plot(tlist[fu:], (results_1tecBala[var_name]*scale)[fu:], color='royalblue', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBala[var_name]*scale)[fu:], color='royalblue', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecRamp[var_name]*scale)[fu:], color='firebrick', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecRamp[var_name]*scale)[fu:], color='firebrick', linestyle='solid')
        elif type == 'diff':
            ax1.plot(tlist[fu:], (results_NoAbat[var_name]  *scale-results_FreeBala[var_name]*scale)[fu:], color='grey')
            ax1.plot(tlist[fu:], (results_1tecBala[var_name]*scale-results_FreeBala[var_name]*scale)[fu:], color='royalblue', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBala[var_name]*scale-results_FreeBala[var_name]*scale)[fu:], color='royalblue', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecBudg[var_name]*scale-results_FreeBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBudg[var_name]*scale-results_FreeBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecRamp[var_name]*scale-results_FreeRamp[var_name]*scale)[fu:], color='firebrick', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecRamp[var_name]*scale-results_FreeRamp[var_name]*scale)[fu:], color='firebrick', linestyle='solid')
        elif type == 'diff2':
            ax1.plot(tlist[fu:], (results_1tecBala[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='royalblue', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBala[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='royalblue', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecBudg[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='darkgreen', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBudg[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='darkgreen', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecRamp[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='firebrick', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecRamp[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='firebrick', linestyle='solid')
    ax1.set_xlim(x1, x2)
    ax1.set_ylim(y1, y2)
    ax1.set_xticks([0, 30, 60, 90, 120, 150])
    plt.show()
    # plt.savefig(f'{name}.ps')
    # plt.clf()
    # """


    # """ Figure S1: learning subsidy
    # ------------------------------------------------------------------------------------------------------------------------------
    table_NoAbat, ip_NoAbat      =  get_csv_content(f_name_categories['no_abate_p0'])
    table_FreeBala, ip_FreeBala  =  get_csv_content(f_name_categories['no_cost_balancing_p0'])
    table_FreeBudg, ip_FreeBudg  =  get_csv_content(f_name_categories['no_cost_budgeting_p0'])
    table_FreeRamp, ip_FreeRamp  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p0'])
    table_1tecBala, ip_1tecBala  =  get_csv_content(f_name_categories['cost_reduction_balancing'][-1])
    table_1tecBudg, ip_1tecBudg  =  get_csv_content(f_name_categories['cost_reduction_budgeting'][-1])
    table_1tecRamp, ip_1tecRamp  =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][-1])
    table_2tecBala, ip_2tecBala  =  get_csv_content(f_name_categories['central_balancing_p0'])
    table_2tecBudg, ip_2tecBudg  =  get_csv_content(f_name_categories['central_budgeting_p0'])
    table_2tecRamp, ip_2tecRamp  =  get_csv_content(f_name_categories['central_budgeting_s_p0'])
    var_to_get = ['tlist', 'eGross', 'abateCostTech_1', 'mcAbateTech_0', 'miuTech_0', 'miuTech_1', 'pBackTime_0', 'pBackTime_1']
    results_2tecBala  =  get_var_from_table(table_2tecBala, var_to_get, ip_2tecBala)
    results_2tecBudg  =  get_var_from_table(table_2tecBudg, var_to_get, ip_2tecBudg)
    results_2tecRamp  =  get_var_from_table(table_2tecRamp, var_to_get, ip_2tecRamp)
    learning_subsidy_Bala = learning_subsidy(results_2tecBala)
    learning_subsidy_Budg = learning_subsidy(results_2tecBudg)
    learning_subsidy_Ramp = learning_subsidy(results_2tecRamp)
    tlist = results_2tecBala['tlist']
    rr = np.exp(-0.03 * tlist)  # prstpVal = 0.03
    plt.plot(tlist, learning_subsidy_Bala, color='royalblue')
    plt.plot(tlist, learning_subsidy_Budg, color='darkgreen')
    plt.plot(tlist, learning_subsidy_Ramp, color='firebrick')
    plt.xlim(0, 150)
    plt.xticks([0, 30, 60, 90, 120, 150])
    plt.ylim(0, 0.5)
    plt.show()
    # plt.savefig(f'ls.ps')
    plt.clf()
    # """


    """ Figure 3 and S6
    # !!!! Need to find the best for each of these ensembles
    # ------------------------------------------------------------------------------------------------------------------------------
    # ['0.01', '0.031623', '0.1', '0.316228', '1', '10.0'] -> $25/tCO2; $79/tCO2; $250/tCO2; $790/tCO2; $2500/tCO2; COIN-abatement
    framing = 2
    table_NoAbat, ip_NoAbat  =  get_csv_content(f_name_categories['no_abate_p0'])
    table_FreeNo, ip_FreeNo  =  get_csv_content(f_name_categories['no_cost_balancing_p0'])
    if framing == 0:
        table_Free,    ip_Free     =  get_csv_content(f_name_categories['no_cost_balancing_p0'])
        table_1tec,    ip_1tec     =  get_csv_content(f_name_categories['cost_reduction_balancing'][-1])
        table_2tec_00, ip_2tec_00  =  get_csv_content(f_name_categories['central_balancing_p0'])
        table_2tec_01, ip_2tec_01  =  get_csv_content(f_name_categories['cost_reduction_balancing'][30])
        table_2tec_02, ip_2tec_02  =  get_csv_content(f_name_categories['cost_reduction_balancing'][20])
        table_2tec_03, ip_2tec_03  =  get_csv_content(f_name_categories['cost_reduction_balancing'][8])
        table_2tec_04, ip_2tec_04  =  get_csv_content(f_name_categories['cost_reduction_balancing'][0])
    if framing == 1:
        table_Free,    ip_Free     =  get_csv_content(f_name_categories['no_cost_budgeting_p0'])
        table_1tec,    ip_1tec     =  get_csv_content(f_name_categories['cost_reduction_budgeting'][-1])
        table_2tec_00, ip_2tec_00  =  get_csv_content(f_name_categories['central_budgeting_p0'])
        table_2tec_01, ip_2tec_01  =  get_csv_content(f_name_categories['cost_reduction_budgeting'][30])
        table_2tec_02, ip_2tec_02  =  get_csv_content(f_name_categories['cost_reduction_budgeting'][20])
        table_2tec_03, ip_2tec_03  =  get_csv_content(f_name_categories['cost_reduction_budgeting'][8])
        table_2tec_04, ip_2tec_04  =  get_csv_content(f_name_categories['cost_reduction_budgeting'][0])
    if framing == 2:
        table_Free,    ip_Free     =  get_csv_content(f_name_categories['no_cost_budgeting_s_p0'])
        table_1tec,    ip_1tec     =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][-1])
        table_2tec_00, ip_2tec_00  =  get_csv_content(f_name_categories['central_budgeting_s_p0'])
        table_2tec_01, ip_2tec_01  =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][30])
        table_2tec_02, ip_2tec_02  =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][20])
        table_2tec_03, ip_2tec_03  =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][8])
        table_2tec_04, ip_2tec_04  =  get_csv_content(f_name_categories['cost_reduction_budgeting_s'][0])

    # Get variable values
    var_to_get = ['tlist', 'eInd', 'abateCost', 'c', 'tatm', 'rsav']
    results_NoAbat   =  get_var_from_table(table_NoAbat,   var_to_get, ip_NoAbat)
    results_FreeNo   =  get_var_from_table(table_FreeNo,   var_to_get, ip_FreeNo)
    results_Free     =  get_var_from_table(table_Free,     var_to_get, ip_Free)
    results_1tec     =  get_var_from_table(table_1tec,     var_to_get, ip_1tec)
    results_2tec_00  =  get_var_from_table(table_2tec_00,  var_to_get, ip_2tec_00)
    results_2tec_01  =  get_var_from_table(table_2tec_01,  var_to_get, ip_2tec_01)
    results_2tec_02  =  get_var_from_table(table_2tec_02,  var_to_get, ip_2tec_02)
    results_2tec_03  =  get_var_from_table(table_2tec_03,  var_to_get, ip_2tec_03)
    results_2tec_04  =  get_var_from_table(table_2tec_04,  var_to_get, ip_2tec_04)
    # # Now plot
    # var_name = 'eInd'; x1=0; x2=150; y1=0; y2=70; scale=40; name='eInd_GtCO2'; type='absolute'; fu=0   # 40 GtCO2 for 100 Trillion $ production in year-0
    # var_name = 'abateCost'; x1=0; x2=150; y1=0; y2=11; scale=100; name='abatement_cost_T$'; type='absolute'; fu=0
    # var_name = 'c'; x1=0; x2=150; y1=0; y2=40; scale=-100; name='consumption_T$'; type='diff'; fu=0
    # var_name = 'tatm'; x1=0; x2=150; y1=0; y2=4; scale=1; name='tatm_K'; type='absolute'; fu=0
    # var_name = 'rsav'; x1=0; x2=150; y1=24; y2=27; scale=100; name='saving_rate_%'; type='absolute'; fu=1
    var_name = 'c'; x1=0; x2=150; y1=-15; y2=40; scale=100; name='consumption_T$'; type='diff2'; fu=1
    tlist = results_NoAbat['tlist']
    ax1 = plt.subplot(111)
    if type == 'absolute':
        ax1.plot(tlist[fu:], (results_NoAbat[var_name]*scale)[fu:],  color='grey')
        ax1.plot(tlist[fu:], (results_1tec[var_name]*scale)[fu:],    color='#B5179E')
        ax1.plot(tlist[fu:], (results_2tec_00[var_name]*scale)[fu:], color='#9B2226')
        ax1.plot(tlist[fu:], (results_2tec_01[var_name]*scale)[fu:], color='#EE9B00')
        ax1.plot(tlist[fu:], (results_2tec_02[var_name]*scale)[fu:], color='#E9D8A6')
        ax1.plot(tlist[fu:], (results_2tec_03[var_name]*scale)[fu:], color='#94D2BD')
        ax1.plot(tlist[fu:], (results_2tec_04[var_name]*scale)[fu:], color='#005F73')
    elif type == 'diff':
        ax1.plot(tlist[fu:], (results_NoAbat[var_name]*scale  -results_FreeNo[var_name]*scale)[fu:], color='grey')
        ax1.plot(tlist[fu:], (results_1tec[var_name]*scale    -results_Free[var_name]*scale)[fu:],   color='#B5179E')
        ax1.plot(tlist[fu:], (results_2tec_00[var_name]*scale -results_Free[var_name]*scale)[fu:],   color='#9B2226')
        ax1.plot(tlist[fu:], (results_2tec_01[var_name]*scale -results_Free[var_name]*scale)[fu:],   color='#EE9B00')
        ax1.plot(tlist[fu:], (results_2tec_02[var_name]*scale -results_Free[var_name]*scale)[fu:],   color='#E9D8A6')
        ax1.plot(tlist[fu:], (results_2tec_03[var_name]*scale -results_Free[var_name]*scale)[fu:],   color='#94D2BD')
        ax1.plot(tlist[fu:], (results_2tec_04[var_name]*scale -results_Free[var_name]*scale)[fu:],   color='#005F73')
    elif type == 'diff2':
        ax1.plot(tlist[fu:], (results_1tec[var_name]*scale    -results_NoAbat[var_name]*scale)[fu:],   color='#B5179E')
        ax1.plot(tlist[fu:], (results_2tec_00[var_name]*scale -results_NoAbat[var_name]*scale)[fu:],   color='#9B2226')
        ax1.plot(tlist[fu:], (results_2tec_01[var_name]*scale -results_NoAbat[var_name]*scale)[fu:],   color='#EE9B00')
        ax1.plot(tlist[fu:], (results_2tec_02[var_name]*scale -results_NoAbat[var_name]*scale)[fu:],   color='#E9D8A6')
        ax1.plot(tlist[fu:], (results_2tec_03[var_name]*scale -results_NoAbat[var_name]*scale)[fu:],   color='#94D2BD')
        ax1.plot(tlist[fu:], (results_2tec_04[var_name]*scale -results_NoAbat[var_name]*scale)[fu:],   color='#005F73')
    ax1.set_xlim(x1, x2)
    ax1.set_ylim(y1, y2)
    ax1.set_xticks([0, 30, 60, 90, 120, 150])
    # plt.show()
    plt.savefig(f'{name}.ps')
    plt.clf()
    # """


    """ Figure S7, changes as a function of the Green Premium
    # ------------------------------------------------------------------------------------------------------------------------------
    var_to_get = ['tlist', 'pBackTime_1', 'cemutotper', 'abateCost', 'damages', 'abateAmount', 'abateAmountTech_1']
    # No abatement case
    table_NoAbat, ip_NoAbat = get_csv_content(f_name_categories['no_abate_p0'])
    results_no  =  get_var_from_table(table_NoAbat, var_to_get, ip_NoAbat)
    no_case_consumption, no_case_carbonemitt = np.sum(results_no['cemutotper']*100), np.sum(results_no['abateAmount']*40)
    def calculate_sum(table_Free, ip_Free, aa):
        results_ref = get_var_from_table(table_Free, var_to_get, ip_Free)
        tlist = results_ref['tlist']
        rr = np.exp(-0.03 * tlist)  # prstpVal = 0.03
        # Now get abatement results
        new_tech_initial_cost_list = []
        new_tech_initial_cost_cons, new_tech_initial_cost_abat, new_tech_initial_cost_dama = [], [], []
        new_tech_initial_cost_etot, new_tech_initial_cost_enew = [], []
        for file in aa:
            table_tmp, ip_tmp  =  get_csv_content(file)
            results_tmp  =  get_var_from_table(table_tmp, var_to_get, ip_tmp)
            new_tech_initial_cost_list = np.r_[new_tech_initial_cost_list, results_tmp['pBackTime_1'][0]]
            new_tech_initial_cost_cons = np.r_[new_tech_initial_cost_cons, np.sum(results_tmp['cemutotper']*100)]
            new_tech_initial_cost_abat = np.r_[new_tech_initial_cost_abat, np.sum(results_tmp['abateCost']*100*rr)]
            new_tech_initial_cost_dama = np.r_[new_tech_initial_cost_dama, np.sum(results_tmp['damages']*100*rr)]
            new_tech_initial_cost_etot = np.r_[new_tech_initial_cost_etot, np.sum(results_tmp['abateAmount']*40*rr)]
            new_tech_initial_cost_enew = np.r_[new_tech_initial_cost_enew, np.sum(results_tmp['abateAmountTech_1']*40*rr)]
        arg_sort = np.argsort(new_tech_initial_cost_list)
        list_sorted = new_tech_initial_cost_list[arg_sort]
        cons_sorted = new_tech_initial_cost_cons[arg_sort]
        abat_sorted = new_tech_initial_cost_abat[arg_sort]
        dama_sorted = new_tech_initial_cost_dama[arg_sort]
        etot_sorted = new_tech_initial_cost_etot[arg_sort]
        enew_sorted = new_tech_initial_cost_enew[arg_sort]
        return list_sorted*2500, cons_sorted-no_case_consumption, abat_sorted, dama_sorted, etot_sorted, enew_sorted
    def plot(ax1, ax2, cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0):
        new_x_axis = np.log10(cost_0[:-1]/2500)
        ax1.plot(new_x_axis, cons_new_tech_0[:-1], color='black')
        ax1.stackplot(new_x_axis, [abat_0[:-1], dama_0[:-1]])
        ax2.plot(new_x_axis, etot_0[:-1], color='firebrick')
        ax2.plot(new_x_axis, enew_0[:-1], color='royalblue')
    # Balancing
    table_Free, ip_Free  =  get_csv_content(f_name_categories['no_cost_balancing_p0'])
    aa = f_name_categories['cost_reduction_balancing']
    cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0 = calculate_sum(table_Free, ip_Free, aa)
    ax1 = plt.subplot(321); ax2 = plt.subplot(322)
    plot(ax1, ax2, cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0)
    # Budgeting
    table_Free, ip_Free  =  get_csv_content(f_name_categories['no_cost_budgeting_p0'])
    aa = f_name_categories['cost_reduction_budgeting']
    cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0 = calculate_sum(table_Free, ip_Free, aa)
    ax3 = plt.subplot(323, sharex=ax1, sharey=ax1); ax4 = plt.subplot(324, sharex=ax2, sharey=ax2)
    plot(ax3, ax4, cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0)
    # Budgeting_s
    table_Free, ip_Free  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p0'])
    aa = f_name_categories['cost_reduction_budgeting_s']
    cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0 = calculate_sum(table_Free, ip_Free, aa)
    ax5 = plt.subplot(325, sharex=ax1, sharey=ax1); ax6 = plt.subplot(326, sharex=ax2, sharey=ax2)
    plot(ax5, ax6, cost_0, cons_new_tech_0, abat_0, dama_0, etot_0, enew_0)
    ax1.set_xlim(-2, 0); ax1.set_ylim(0, 150);   ax1.set_yticks([0, 50, 100, 150])
    ax2.set_xlim(-2, 0); ax2.set_ylim(0, 1500);  ax2.set_yticks([0, 500, 1000, 1500])
    # plt.show()
    plt.savefig('s7.ps')
    plt.clf()  
    # """



    """ Figure 4 
    # ------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------
    pre_balancing_list = f_name_categories['free_abate_balancing']
    pre_budgetint_list = f_name_categories['free_abate_budgeting']
    pre_budgeting_s_list = f_name_categories['free_abate_budgeting_s']

    def calculate_sum(table_Free, ip_Free, aa, bb):
        var_to_get = ['tlist', 'pBackTime_1', 'abateCost', 'damages', 'cemutotper']
        # Get free abatement results, tlist, and rr here:
        results_ref  =  get_var_from_table(table_Free, var_to_get, ip_Free)
        tlist = results_ref['tlist']
        rr = np.exp(-0.03 * tlist)  # prstpVal = 0.03
        # Now get abatement results
        new_tech_initial_cost_list = []
        new_tech_initial_cost_cons = []
        for file in aa:
            table_tmp, ip_tmp  =  get_csv_content(file)
            results_tmp  =  get_var_from_table(table_tmp, var_to_get, ip_tmp)
            new_tech_initial_cost_list = np.r_[new_tech_initial_cost_list, results_tmp['pBackTime_1'][0]]
            new_tech_initial_cost_cons = np.r_[new_tech_initial_cost_cons, np.sum(results_tmp['cemutotper']*100)]
        arg_sort = np.argsort(new_tech_initial_cost_list)
        new_tech_initial_cost_list_sorted = new_tech_initial_cost_list[arg_sort]
        new_tech_initial_cost_cons_sorted = new_tech_initial_cost_cons[arg_sort]
        cost_fraction = (new_tech_initial_cost_list_sorted[-2] - new_tech_initial_cost_list_sorted) / new_tech_initial_cost_list_sorted[-2] * 100
        new_tech_initial_cons_decrea = new_tech_initial_cost_cons_sorted - new_tech_initial_cost_cons_sorted[-2]
        # Now get pre-abate results 
        pre_abatement_cons = []
        for file in bb:
            table_tmp, ip_tmp  =  get_csv_content(file)
            results_tmp  =  get_var_from_table(table_tmp, var_to_get, ip_tmp)
            pre_abatement_cons = np.r_[pre_abatement_cons, np.sum(results_tmp['cemutotper']*100)]
        pre_abatement_cons_decrea = pre_abatement_cons - pre_abatement_cons[0]
        return cost_fraction, new_tech_initial_cons_decrea, pre_abatement_cons_decrea

    table_NoAbat, ip_NoAbat  =  get_csv_content(f_name_categories['no_abate_p0'])
    # Balancing
    table_Free, ip_Free  =  get_csv_content(f_name_categories['no_cost_balancing_p0'])
    aa = f_name_categories['cost_reduction_balancing']
    bb = pre_balancing_list
    cost0, cons_new_tech_0, cons_pre_abatement_0 = calculate_sum(table_Free, ip_Free, aa, bb)
    # Budgeting
    table_Free, ip_Free  =  get_csv_content(f_name_categories['no_cost_budgeting_p0'])
    aa = f_name_categories['cost_reduction_budgeting']
    bb = pre_budgetint_list
    cost1, cons_new_tech_1, cons_pre_abatement_1 = calculate_sum(table_Free, ip_Free, aa, bb)
    # Budgeting_s
    table_Free, ip_Free  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p0'])
    aa = f_name_categories['cost_reduction_budgeting_s']
    bb = pre_budgeting_s_list
    cost2, cons_new_tech_2, cons_pre_abatement_2 = calculate_sum(table_Free, ip_Free, aa, bb) 

    ax1 = plt.subplot(111)
    ax1.plot( np.array(cost0[:-1]), np.array(cons_new_tech_0[:-1]),  color='royalblue') 
    ax1.plot( np.array(cost1[:-1]), np.array(cons_new_tech_1[:-1]),  color='darkgreen') 
    ax1.plot( np.array(cost2[:-1]), np.array(cons_new_tech_2[:-1]),  color='firebrick') 
    ax1.set_xlim(0, 100); ax1.set_xticks([0, 20, 40, 60, 80, 100])
    ax1.set_ylim(0, 150); ax1.set_yticks([0, 50, 100, 150])
    # plt.show()
    plt.savefig('fig4_p1.ps')
    plt.clf()

    ax2 = plt.subplot(111)
    x_axis = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]) * 40
    ax2.plot( x_axis, np.array(cons_pre_abatement_0),  color='royalblue') 
    ax2.plot( x_axis, np.array(cons_pre_abatement_1),  color='darkgreen') 
    ax2.plot( x_axis, np.array(cons_pre_abatement_2),  color='firebrick') 
    ax2.set_xlim(0, 8000); ax2.set_xticks([0, 2000, 4000, 6000, 8000])
    ax2.set_ylim(0, 150); ax2.set_yticks([0, 50, 100, 150])
    # plt.show()
    plt.savefig('fig4_p2.ps')
    plt.clf()
    
    ### Interpolation starts:
    from scipy import interpolate
    intepo_kind = 'cubic'
    f_INNO_balancing = interpolate.interp1d(cons_new_tech_0[:-1][::-1], cost0[:-1][::-1], kind=intepo_kind); from_INNO_balancing = f_INNO_balancing(np.arange(0, 50, 1))
    f_FREE_balancing = interpolate.interp1d(cons_pre_abatement_0,       x_axis,           kind=intepo_kind); from_FREE_balancing = f_FREE_balancing(np.arange(0, 50, 1))
    f_INNO_budgeting = interpolate.interp1d(cons_new_tech_1[:-1][::-1], cost1[:-1][::-1], kind=intepo_kind); from_INNO_budgeting = f_INNO_budgeting(np.arange(0, 50, 1))
    f_FREE_budgeting = interpolate.interp1d(cons_pre_abatement_1,       x_axis,           kind=intepo_kind); from_FREE_budgeting = f_FREE_budgeting(np.arange(0, 50, 1))
    f_INNO_rampinggg = interpolate.interp1d(cons_new_tech_2[:-1][::-1], cost2[:-1][::-1], kind=intepo_kind); from_INNO_rampinggg = f_INNO_rampinggg(np.arange(0, 120, 1))
    f_FREE_rampinggg = interpolate.interp1d(cons_pre_abatement_2,       x_axis,           kind=intepo_kind); from_FREE_rampinggg = f_FREE_rampinggg(np.arange(0, 120, 1))
    ax3 = plt.subplot(111)
    ax3.plot( np.array(from_INNO_balancing), np.array(from_FREE_balancing),  color='royalblue') 
    ax3.plot( np.array(from_INNO_budgeting), np.array(from_FREE_budgeting),  color='darkgreen') 
    ax3.plot( np.array(from_INNO_rampinggg), np.array(from_FREE_rampinggg),  color='firebrick') 
    ax3.set_xlim(0, 100); ax3.set_xticks([0, 20, 40, 60, 80, 100])
    ax3.set_ylim(0, 2500); ax3.set_yticks([0, 500, 1000, 1500, 2000])
    # plt.show()
    plt.savefig('fig4_p3.ps')
    plt.clf()
    # """



    """ Figure S8, NPV of key parameters for main cases 
    # ------------------------------------------------------------------------------------------------------------------------------
    def get_results(table_in, table_in_2 = 0):
        tlist = table_in['tlist']
        rr = np.exp(-0.03 * tlist)  # prstpVal = 0.03
        abatement_cost = np.sum(table_in['abateCost'] * rr * 100)
        climate_damage = np.sum(table_in['damages'] * rr * 100)
        to_consumption = np.sum(table_in['cemutotper'] * 100)
        if table_in_2 != 0:
            ls_tmp = learning_subsidy(table_in_2)
            ls = np.sum(ls_tmp * rr)
        else:
            ls = 0
        return abatement_cost, climate_damage, to_consumption, ls
    def plot(abatement_cost0, climate_damage0, to_consumption0, ls_sum0, abatement_cost1, climate_damage1, to_consumption1, ls_sum1, num):
        x = ls_sum0-ls_sum1
        plt.bar(num, x, color='orange')
        a = (abatement_cost0-abatement_cost1) - x
        plt.bar(num, a, color='green', bottom=x)
        b = climate_damage0-climate_damage1
        plt.bar(num, b, color='grey', bottom=x+a)
        c = (to_consumption1-to_consumption0) - (abatement_cost0-abatement_cost1) - (climate_damage0-climate_damage1)
        plt.bar(num, c, color='blue', bottom=x+a+b)

    def start(file_ref, flag_ref, file_chg, flag_chg, num):
        var_to_get1 = ['tlist', 'eInd', 'tatm', 'abateCost', 'damages', 'cemutotper']
        var_to_get2 = ['tlist', 'abateCostTech_1', 'mcAbateTech_0', 'mcAbateTech_1', 'miuTech_0', 'miuTech_1', 'pBackTime_0', 'pBackTime_1', 'eGross']
        table_ref, ip_ref  =  get_csv_content(file_ref)
        results_ref_base = get_var_from_table(table_ref, var_to_get1, ip_ref)
        results_ref_newtech = 0 if flag_ref == 0 else get_var_from_table(table_ref, var_to_get2, ip_ref) 
        table_chg, ip_chg  =  get_csv_content(file_chg)
        results_chg_base = get_var_from_table(table_chg, var_to_get1, ip_chg)
        results_chg_newtech = 0 if flag_chg == 0 else get_var_from_table(table_chg, var_to_get2, ip_chg)  
        abatement_cost_ref, climate_damage_ref, to_consumption_ref, ls_ref = get_results(results_ref_base, results_ref_newtech)
        abatement_cost_chg, climate_damage_chg, to_consumption_chg, ls_chg = get_results(results_chg_base, results_chg_newtech)
        plot(abatement_cost_chg, climate_damage_chg, to_consumption_chg, ls_chg, abatement_cost_ref, climate_damage_ref, to_consumption_ref, ls_ref, num)
    start(f_name_categories['no_cost_balancing_p0'],     0, f_name_categories['no_abate_p0'],                       0,   0)
    start(f_name_categories['no_cost_balancing_p0'],     0, f_name_categories['cost_reduction_balancing'][-1],      1,   2)
    start(f_name_categories['no_cost_balancing_p0'],     0, f_name_categories['central_balancing_p0'],              1,   3)
    start(f_name_categories['no_cost_budgeting_p0'],     0, f_name_categories['cost_reduction_budgeting'][-1],      1,   5)
    start(f_name_categories['no_cost_budgeting_p0'],     0, f_name_categories['central_budgeting_p0'],              1,   6)
    start(f_name_categories['no_cost_budgeting_s_p0'],   0, f_name_categories['cost_reduction_budgeting_s'][-1],    1,   8)
    start(f_name_categories['no_cost_budgeting_s_p0'],   0, f_name_categories['central_budgeting_s_p0'],            1,   9)
    plt.xticks([0, 2,3, 5,6, 8,9])
    plt.ylim(0, 200)
    # plt.show()
    plt.savefig('f8.ps')
    plt.clf()
    # """



    """ Figure SX, population growth
    # ------------------------------------------------------------------------------------------------------------------------------
    var_to_get = ['tlist', 'eInd', 'tatm', 'abateCost', 'damages', 'c']
    
    # table_NoAbat, ip_NoAbat      =  get_csv_content(f_name_categories['no_abate_p0']);               results_NoAbat    =  get_var_from_table(table_NoAbat, var_to_get, ip_NoAbat)
    # table_FreeBala, ip_FreeBala  =  get_csv_content(f_name_categories['no_cost_balancing_p0']);      results_FreeBala  =  get_var_from_table(table_FreeBala, var_to_get, ip_FreeBala)
    # table_FreeBudg, ip_FreeBudg  =  get_csv_content(f_name_categories['no_cost_budgeting_p0']);      results_FreeBudg  =  get_var_from_table(table_FreeBudg, var_to_get, ip_FreeBudg)
    # table_FreeRamp, ip_FreeRamp  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p0']);    results_FreeRamp  =  get_var_from_table(table_FreeRamp, var_to_get, ip_FreeRamp)
    # table_1tecBala, ip_1tecBala  =  get_csv_content(f_name_categories['1-tech_balancing_p0']);       results_1tecBala  =  get_var_from_table(table_1tecBala, var_to_get, ip_1tecBala)
    # table_1tecBudg, ip_1tecBudg  =  get_csv_content(f_name_categories['1-tech_budgeting_p0']);       results_1tecBudg  =  get_var_from_table(table_1tecBudg, var_to_get, ip_1tecBudg)
    # table_1tecRamp, ip_1tecRamp  =  get_csv_content(f_name_categories['1-tech_budgeting_s_p0']);     results_1tecRamp  =  get_var_from_table(table_1tecRamp, var_to_get, ip_1tecRamp)
    # table_2tecBala, ip_2tecBala  =  get_csv_content(f_name_categories['central_balancing_p0']);      results_2tecBala  =  get_var_from_table(table_2tecBala, var_to_get, ip_2tecBala)
    # table_2tecBudg, ip_2tecBudg  =  get_csv_content(f_name_categories['central_budgeting_p0']);      results_2tecBudg  =  get_var_from_table(table_2tecBudg, var_to_get, ip_2tecBudg)
    # table_2tecRamp, ip_2tecRamp  =  get_csv_content(f_name_categories['central_budgeting_s_p0']);    results_2tecRamp  =  get_var_from_table(table_2tecRamp, var_to_get, ip_2tecRamp)

    # table_NoAbat, ip_NoAbat      =  get_csv_content(f_name_categories['no_abate_p1']);               results_NoAbat    =  get_var_from_table(table_NoAbat, var_to_get, ip_NoAbat)
    # table_FreeBala, ip_FreeBala  =  get_csv_content(f_name_categories['no_cost_balancing_p1']);      results_FreeBala  =  get_var_from_table(table_FreeBala, var_to_get, ip_FreeBala)
    # table_FreeBudg, ip_FreeBudg  =  get_csv_content(f_name_categories['no_cost_budgeting_p1']);      results_FreeBudg  =  get_var_from_table(table_FreeBudg, var_to_get, ip_FreeBudg)
    # table_FreeRamp, ip_FreeRamp  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p1']);    results_FreeRamp  =  get_var_from_table(table_FreeRamp, var_to_get, ip_FreeRamp)
    # table_1tecBala, ip_1tecBala  =  get_csv_content(f_name_categories['1-tech_balancing_p1']);       results_1tecBala  =  get_var_from_table(table_1tecBala, var_to_get, ip_1tecBala)
    # table_1tecBudg, ip_1tecBudg  =  get_csv_content(f_name_categories['1-tech_budgeting_p1']);       results_1tecBudg  =  get_var_from_table(table_1tecBudg, var_to_get, ip_1tecBudg)
    # table_1tecRamp, ip_1tecRamp  =  get_csv_content(f_name_categories['1-tech_budgeting_s_p1']);     results_1tecRamp  =  get_var_from_table(table_1tecRamp, var_to_get, ip_1tecRamp)
    # table_2tecBala, ip_2tecBala  =  get_csv_content(f_name_categories['central_balancing_p1']);      results_2tecBala  =  get_var_from_table(table_2tecBala, var_to_get, ip_2tecBala)
    # table_2tecBudg, ip_2tecBudg  =  get_csv_content(f_name_categories['central_budgeting_p1']);      results_2tecBudg  =  get_var_from_table(table_2tecBudg, var_to_get, ip_2tecBudg)
    # table_2tecRamp, ip_2tecRamp  =  get_csv_content(f_name_categories['central_budgeting_s_p1']);    results_2tecRamp  =  get_var_from_table(table_2tecRamp, var_to_get, ip_2tecRamp)

    table_NoAbat, ip_NoAbat      =  get_csv_content(f_name_categories['no_abate_p2']);               results_NoAbat    =  get_var_from_table(table_NoAbat, var_to_get, ip_NoAbat)
    table_FreeBala, ip_FreeBala  =  get_csv_content(f_name_categories['no_cost_balancing_p2']);      results_FreeBala  =  get_var_from_table(table_FreeBala, var_to_get, ip_FreeBala)
    table_FreeBudg, ip_FreeBudg  =  get_csv_content(f_name_categories['no_cost_budgeting_p2']);      results_FreeBudg  =  get_var_from_table(table_FreeBudg, var_to_get, ip_FreeBudg)
    table_FreeRamp, ip_FreeRamp  =  get_csv_content(f_name_categories['no_cost_budgeting_s_p2']);    results_FreeRamp  =  get_var_from_table(table_FreeRamp, var_to_get, ip_FreeRamp)
    table_1tecBala, ip_1tecBala  =  get_csv_content(f_name_categories['1-tech_balancing_p2']);       results_1tecBala  =  get_var_from_table(table_1tecBala, var_to_get, ip_1tecBala)
    table_1tecBudg, ip_1tecBudg  =  get_csv_content(f_name_categories['1-tech_budgeting_p2']);       results_1tecBudg  =  get_var_from_table(table_1tecBudg, var_to_get, ip_1tecBudg)
    table_1tecRamp, ip_1tecRamp  =  get_csv_content(f_name_categories['1-tech_budgeting_s_p2']);     results_1tecRamp  =  get_var_from_table(table_1tecRamp, var_to_get, ip_1tecRamp)
    table_2tecBala, ip_2tecBala  =  get_csv_content(f_name_categories['central_balancing_p2']);      results_2tecBala  =  get_var_from_table(table_2tecBala, var_to_get, ip_2tecBala)
    table_2tecBudg, ip_2tecBudg  =  get_csv_content(f_name_categories['central_budgeting_p2']);      results_2tecBudg  =  get_var_from_table(table_2tecBudg, var_to_get, ip_2tecBudg)
    table_2tecRamp, ip_2tecRamp  =  get_csv_content(f_name_categories['central_budgeting_s_p2']);    results_2tecRamp  =  get_var_from_table(table_2tecRamp, var_to_get, ip_2tecRamp)




    # ################################# Fig2:
    # var_name = 'eInd'; x1=0; x2=150; y1=0; y2=100; scale=40; name='eInd_GtCO2'; type='absolute'; fu=0
    # var_name = 'tatm'; x1=0; x2=150; y1=0; y2=6; scale=1; name='tatm_K'; type='absolute'; fu=0
    var_name = 'abateCost'; x1=0; x2=150; y1=0; y2=20; scale=100; name='abatement_cost_T$'; type='absolute'; fu=0
    # var_name = 'c'; x1=0; x2=150; y1=0; y2=40; scale=-100; name='consumption_T$'; type='diff'; fu=0
    
    tlist = results_NoAbat['tlist']
    if type == 'multi':
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
        ax1.plot(tlist, results_1tecBala[var_name[0]]*scale, color='royalblue', linestyle='--')
        ax1.plot(tlist, results_1tecBudg[var_name[0]]*scale, color='#483434', linestyle='--')
        ax1.plot(tlist, results_1tecRamp[var_name[0]]*scale, color='firebrick', linestyle='--')
        ax2.plot(tlist, results_2tecBala[var_name[0]]*scale, color='royalblue', linestyle='--')
        ax2.plot(tlist, results_2tecBudg[var_name[0]]*scale, color='#483434', linestyle='--')
        ax2.plot(tlist, results_2tecRamp[var_name[0]]*scale, color='firebrick', linestyle='--')
        ax2.plot(tlist, results_2tecBala[var_name[1]]*scale, color='royalblue', linestyle='solid')
        ax2.plot(tlist, results_2tecBudg[var_name[1]]*scale, color='#483434', linestyle='solid')
        ax2.plot(tlist, results_2tecRamp[var_name[1]]*scale, color='firebrick', linestyle='solid')
    else:
        ax1 = plt.subplot(111)
        if type == 'absolute':
            ax1.plot(tlist[fu:], (results_NoAbat[var_name]*scale)[fu:], color='grey')
            ax1.plot(tlist[fu:], (results_1tecBala[var_name]*scale)[fu:], color='royalblue', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBala[var_name]*scale)[fu:], color='royalblue', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecRamp[var_name]*scale)[fu:], color='firebrick', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecRamp[var_name]*scale)[fu:], color='firebrick', linestyle='solid')
        elif type == 'diff':
            ax1.plot(tlist[fu:], (results_NoAbat[var_name]  *scale-results_FreeBala[var_name]*scale)[fu:], color='grey')
            ax1.plot(tlist[fu:], (results_1tecBala[var_name]*scale-results_FreeBala[var_name]*scale)[fu:], color='royalblue', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBala[var_name]*scale-results_FreeBala[var_name]*scale)[fu:], color='royalblue', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecBudg[var_name]*scale-results_FreeBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBudg[var_name]*scale-results_FreeBudg[var_name]*scale)[fu:], color='darkgreen', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecRamp[var_name]*scale-results_FreeRamp[var_name]*scale)[fu:], color='firebrick', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecRamp[var_name]*scale-results_FreeRamp[var_name]*scale)[fu:], color='firebrick', linestyle='solid')
        elif type == 'diff2':
            ax1.plot(tlist[fu:], (results_1tecBala[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='royalblue', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBala[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='royalblue', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecBudg[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='darkgreen', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecBudg[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='darkgreen', linestyle='solid')
            ax1.plot(tlist[fu:], (results_1tecRamp[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='firebrick', linestyle='--')
            ax1.plot(tlist[fu:], (results_2tecRamp[var_name]*scale-results_NoAbat[var_name]*scale)[fu:], color='firebrick', linestyle='solid')
    ax1.set_xlim(x1, x2)
    ax1.set_ylim(y1, y2)
    ax1.set_xticks([0, 30, 60, 90, 120, 150])
    # plt.show()
    plt.savefig(f'{name}.ps')
    plt.clf()
    # """


    """ Figure SX, Population curve
    # ------------------------------------------------------------------------------------------------------------------------------
    def calculate_population_inputs( T, pop0, popasym, popadj ):
        # Population (individuals)
        L = int(T) * [None]
        L[0] = pop0
        for i in range(1, int(T)): # DICE-2016
            L[i] = L[i-1] * (popasym/L[i-1])**popadj
        return L 
    T = 300
    pop0 = 1
    popasym = 1.5
    popadj_1 = 0.02
    popadj_2 = 0.1
    ll1 = calculate_population_inputs( T, pop0, popasym, popadj_1 )
    ll2 = calculate_population_inputs( T, pop0, popasym, popadj_2 )
    ll3 = pop0 * np.exp(0.0015 * np.arange(T))
    # plt.plot(np.arange(T), np.ones(T), color='black')
    # plt.plot(np.arange(T), ll1, color='black')
    # plt.plot(np.arange(T), ll2, color='black')
    plt.plot(np.arange(T), ll3, color='black')
    plt.xlim(0, 150)
    plt.ylim(0.8, 1.6)
    plt.xticks([0, 30, 60, 90, 120, 150])
    plt.show()
    # plt.savefig('pop.ps')
    plt.clf() 
    # """



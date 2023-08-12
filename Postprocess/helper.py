"""

This script contains functions used in the main calculations

# get_f_name_list: Get lists of model output names for different framings;

"""

import os, csv
import numpy as np
import pickle 



# ---------------------------   Find the best one case  --------------------------- #

def get_var(file_type, var_name, current_table):
    variable_coinver = { 'cemutotper':[3, 'cemutotper'] }
    lis_to_use = variable_coinver
    Table_idx = lis_to_use[var_name][0]
    Varia_idx = lis_to_use[var_name][1]
    var_to_get = current_table[Table_idx][Varia_idx]
    return var_to_get

def select_ensemble(data_path, i):
    fname, fcons = [], []
    for file in i:
        f_name = f'{data_path}{file}'
        with open(f_name, 'rb') as db:
            data = pickle.load(db)
        y = get_var('COIN', 'cemutotper', data)
        f_cons = np.sum(y)
        fname.append(file)
        fcons.append(f_cons)
    argmax_list = np.argmax(fcons)
    print ()
    print (argmax_list, '------', fname[argmax_list], fcons[argmax_list])
    print () 

def find_best(case_name, data_path):

    if case_name == 'no_abate':
        for i in [1, 2]:
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_no-abate_p-{str(i)}_c-no_abate_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
    
    if case_name == 'no_cost':
        for i in [1, 2]:
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_no-cost_p-{str(i)}_c-balancing_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_no-cost_p-{str(i)}_c-budgeting_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
        
        for i in [0, 1, 2]:
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_no-cost_p-{str(i)}_c-budgeting_s_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)

    if case_name == 'central':
        
        for i in [1, 2]: 
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-balancing_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-budgeting_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-budgeting_s_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
        
        for i in [0]: 
            to_check_list = [] 
            for seed in range(3008, 3057, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-budgeting_s_i-1.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)

    if case_name == 'cost_reduction':
        initCostList = np.insert(np.round(10.**-np.arange(0,2.05,0.05),6),0,10)
        for i in initCostList:
            to_check_list = [] 
            for seed in range(3008, 3017, 1): 
                to_check_name = f'COIN_020_central_p-0_c-budgeting_s_i-{str(i)}_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)

    if case_name == 'free_abate':
        freeAbateVals = [10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,120.,140.,160.,180.,200.] 
        for i in freeAbateVals:
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-{str(i)}_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
    
    if case_name == '1-tech':
        for i in [1, 2]:
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-balancing_i-10.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-budgeting_i-10.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)
            to_check_list = [] 
            for seed in range(3008, 3017, 1):
                to_check_name = f'COIN_020_central_p-{str(i)}_c-budgeting_s_i-10.0_f-0.0_s-{str(seed)}_m-100000.pickle'
                to_check_list.append(to_check_name)
            select_ensemble(data_path, to_check_list)



def get_f_name_list(csv_ken_path, csv_ken_free, csv_lei_path):

    f_name_categories  =  {}
    file_list_csv_ken_path = os.listdir(csv_ken_path)
    file_list_csv_ken_free = os.listdir(csv_ken_free)
    file_list_csv_lei_path = os.listdir(csv_lei_path)

    #### (1) No abate case, one used for all 
    # find_best('no_abate', csv_lei_path)
    f_name_categories['no_abate_p0'] = csv_ken_path + 'COIN_018_no-abate_c-ramping_i-1.0_s-14_m-100000.CSV'
    f_name_categories['no_abate_p1'] = csv_lei_path + 'COIN_020_no-abate_p-1_c-no_abate_i-1.0_f-0.0_s-3013_m-100000.CSV'
    f_name_categories['no_abate_p2'] = csv_lei_path + 'COIN_020_no-abate_p-2_c-no_abate_i-1.0_f-0.0_s-3008_m-100000.CSV'

    #### (2) No cost case
    # find_best('no_cost', csv_lei_path)
    f_name_categories['no_cost_balancing_p0'] = csv_ken_path + 'COIN_018_no-cost_c-balancing_i-1.0_s-5_m-100000.CSV'
    f_name_categories['no_cost_balancing_p1'] = csv_lei_path + 'COIN_020_no-cost_p-1_c-balancing_i-1.0_f-0.0_s-3012_m-100000.CSV'
    f_name_categories['no_cost_balancing_p2'] = csv_lei_path + 'COIN_020_no-cost_p-2_c-balancing_i-1.0_f-0.0_s-3012_m-100000.CSV'
    f_name_categories['no_cost_budgeting_p0'] = csv_ken_path + 'COIN_018_no-cost_c-budgeting_i-1.0_s-16_m-100000.CSV'
    f_name_categories['no_cost_budgeting_p1'] = csv_lei_path + 'COIN_020_no-cost_p-1_c-budgeting_i-1.0_f-0.0_s-3009_m-100000.CSV'
    f_name_categories['no_cost_budgeting_p2'] = csv_lei_path + 'COIN_020_no-cost_p-2_c-budgeting_i-1.0_f-0.0_s-3016_m-100000.CSV'
    f_name_categories['no_cost_budgeting_s_p0'] = csv_lei_path + 'COIN_020_no-cost_p-0_c-budgeting_s_i-1.0_f-0.0_s-3015_m-100000.CSV'
    f_name_categories['no_cost_budgeting_s_p1'] = csv_lei_path + 'COIN_020_no-cost_p-1_c-budgeting_s_i-1.0_f-0.0_s-3008_m-100000.CSV'
    f_name_categories['no_cost_budgeting_s_p2'] = csv_lei_path + 'COIN_020_no-cost_p-2_c-budgeting_s_i-1.0_f-0.0_s-3013_m-100000.CSV'

    #### (3) Central case
    # find_best('central', csv_lei_path)
    f_name_categories['central_balancing_p0'] = csv_ken_path + 'COIN_018_central_c-balancing_i-1_s-4_m-100000.CSV'
    f_name_categories['central_balancing_p1'] = csv_lei_path + 'COIN_020_central_p-1_c-balancing_i-1.0_f-0.0_s-3016_m-100000.CSV'
    f_name_categories['central_balancing_p2'] = csv_lei_path + 'COIN_020_central_p-2_c-balancing_i-1.0_f-0.0_s-3014_m-100000.CSV'
    f_name_categories['central_budgeting_p0'] = csv_ken_path + 'COIN_018_central_c-budgeting_i-1.0_s-304_m-100000.CSV'
    f_name_categories['central_budgeting_p1'] = csv_lei_path + 'COIN_020_central_p-1_c-budgeting_i-1.0_f-0.0_s-3016_m-100000.CSV'
    f_name_categories['central_budgeting_p2'] = csv_lei_path + 'COIN_020_central_p-2_c-budgeting_i-1.0_f-0.0_s-3012_m-100000.CSV'
    f_name_categories['central_budgeting_s_p0'] = csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-1.0_f-0.0_s-3008_m-100000.CSV'
    f_name_categories['central_budgeting_s_p1'] = csv_lei_path + 'COIN_020_central_p-1_c-budgeting_s_i-1.0_f-0.0_s-3008_m-100000.CSV'
    f_name_categories['central_budgeting_s_p2'] = csv_lei_path + 'COIN_020_central_p-2_c-budgeting_s_i-1.0_f-0.0_s-3011_m-100000.CSV'



    #### (4) Cost reduction case
    # find_best('cost_reduction', csv_lei_path)
    f_name_categories['cost_reduction_balancing'] = [csv_ken_path + 'COIN_018_central_c-balancing_i-0.01_s-417_m-100000.CSV',      csv_ken_path + 'COIN_018_central_c-balancing_i-0.01122_s-455_m-100000.CSV',    csv_ken_path + 'COIN_018_central_c-balancing_i-0.012589_s-455_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.014125_s-461_m-100000.CSV', 
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.015849_s-25_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.017783_s-430_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.019953_s-20_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.022387_s-461_m-100000.CSV', 
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.025119_s-460_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.028184_s-461_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.031623_s-461_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.035481_s-440_m-100000.CSV', 
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.039811_s-440_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.044668_s-451_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.050119_s-451_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.056234_s-24_m-100000.CSV', 
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.063096_s-440_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.070795_s-20_m-100000.CSV',    csv_ken_path + 'COIN_018_central_c-balancing_i-0.079433_s-460_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.089125_s-451_m-100000.CSV', 
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.1_s-416_m-100000.CSV',       csv_ken_path + 'COIN_018_central_c-balancing_i-0.112202_s-435_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.125893_s-20_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.141254_s-435_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.158489_s-461_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.177828_s-451_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.199526_s-440_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.223872_s-440_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.251189_s-440_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.281838_s-456_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.316228_s-452_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.354813_s-462_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.398107_s-26_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.446684_s-440_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.501187_s-455_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.562341_s-462_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-0.630957_s-452_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.707946_s-452_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-balancing_i-0.794328_s-457_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-balancing_i-0.891251_s-457_m-100000.CSV', 
                                                     csv_ken_path + 'COIN_018_central_c-balancing_i-1_s-4_m-100000.CSV',           csv_ken_path + 'COIN_018_central_c-balancing_i-10.0_s-67_m-100000.CSV']
    f_name_categories['cost_reduction_budgeting'] = [csv_ken_path + 'COIN_018_central_c-budgeting_i-0.01_s-422_m-100000.CSV',      csv_ken_path + 'COIN_018_central_c-budgeting_i-0.01122_s-456_m-100000.CSV',    csv_ken_path + 'COIN_018_central_c-budgeting_i-0.012589_s-20_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.014125_s-461_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.015849_s-430_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.017783_s-24_m-100000.CSV',    csv_ken_path + 'COIN_018_central_c-budgeting_i-0.019953_s-435_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.022387_s-456_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.025119_s-460_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.028184_s-451_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.031623_s-417_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.035481_s-450_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.039811_s-435_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.044668_s-20_m-100000.CSV',    csv_ken_path + 'COIN_018_central_c-budgeting_i-0.050119_s-460_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.056234_s-451_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.063096_s-451_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.070795_s-451_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.079433_s-455_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.089125_s-451_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.1_s-404_m-100000.CSV',       csv_ken_path + 'COIN_018_central_c-budgeting_i-0.112202_s-450_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.125893_s-435_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.141254_s-455_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.158489_s-430_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.177828_s-451_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.199526_s-450_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.223872_s-25_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.251189_s-440_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.281838_s-25_m-100000.CSV',    csv_ken_path + 'COIN_018_central_c-budgeting_i-0.316228_s-404_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.354813_s-452_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.398107_s-435_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.446684_s-435_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.501187_s-440_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.562341_s-24_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-0.630957_s-435_m-100000.CSV',  csv_ken_path + 'COIN_018_central_c-budgeting_i-0.707946_s-460_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.794328_s-23_m-100000.CSV',   csv_ken_path + 'COIN_018_central_c-budgeting_i-0.891251_s-431_m-100000.CSV',
                                                     csv_ken_path + 'COIN_018_central_c-budgeting_i-1.0_s-304_m-100000.CSV',       csv_ken_path + 'COIN_018_central_c-budgeting_i-10.0_s-16_m-100000.CSV']
    f_name_categories['cost_reduction_budgeting_s'] = [csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.01_f-0.0_s-3012_m-100000.CSV',       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.01122_f-0.0_s-3013_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.012589_f-0.0_s-3010_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.014125_f-0.0_s-3012_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.015849_f-0.0_s-3009_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.017783_f-0.0_s-3015_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.019953_f-0.0_s-3011_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.022387_f-0.0_s-3012_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.025119_f-0.0_s-3013_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.028184_f-0.0_s-3011_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.031623_f-0.0_s-3014_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.035481_f-0.0_s-3008_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.039811_f-0.0_s-3011_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.044668_f-0.0_s-3012_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.050119_f-0.0_s-3012_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.056234_f-0.0_s-3014_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.063096_f-0.0_s-3013_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.070795_f-0.0_s-3008_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.079433_f-0.0_s-3012_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.089125_f-0.0_s-3008_m-100000.CSV',
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.1_f-0.0_s-3008_m-100000.CSV',        csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.112202_f-0.0_s-3015_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.125893_f-0.0_s-3014_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.141254_f-0.0_s-3013_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.158489_f-0.0_s-3014_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.177828_f-0.0_s-3010_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.199526_f-0.0_s-3008_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.223872_f-0.0_s-3012_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.251189_f-0.0_s-3010_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.281838_f-0.0_s-3008_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.316228_f-0.0_s-3010_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.354813_f-0.0_s-3008_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.398107_f-0.0_s-3014_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.446684_f-0.0_s-3010_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.501187_f-0.0_s-3010_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.562341_f-0.0_s-3015_m-100000.CSV', 
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.630957_f-0.0_s-3012_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.707946_f-0.0_s-3008_m-100000.CSV',  csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.794328_f-0.0_s-3016_m-100000.CSV',   csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-0.891251_f-0.0_s-3008_m-100000.CSV',
                                                       csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-1.0_f-0.0_s-3008_m-100000.CSV',        csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-10.0_f-0.0_s-3010_m-100000.CSV']

    #### (4) Free abatement case
    # find_best('free_abate', csv_lei_path)
    f_name_categories['free_abate_balancing'] = [csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-0_s-4082_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-10_s-3042_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-20_s-3053_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-30_s-3024_m-500000.CSV',
                                                 csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-40_s-3066_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-50_s-3022_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-60_s-3053_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-70_s-3047_m-500000.CSV',
                                                 csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-80_s-3021_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-90_s-3022_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-100_s-3059_m-500000.CSV',  csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-120_s-3063_m-500000.CSV',
                                                 csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-140_s-3026_m-500000.CSV',  csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-160_s-3019_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-180_s-4071_m-500000.CSV',  csv_ken_free + 'COIN_018.2_central_c-balancing_i-1.0_f-200_s-3022_m-500000.CSV']

    f_name_categories['free_abate_budgeting'] = [csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-0_s-3032_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-10_s-3071_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-20_s-3050_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-30_s-3073_m-500000.CSV',
                                                 csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-40_s-3070_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-50_s-3018_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-60_s-3053_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-70_s-3010_m-500000.CSV',
                                                 csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-80_s-3069_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-90_s-4200_m-500000.CSV',    csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-100_s-3022_m-500000.CSV',  csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-120_s-3026_m-500000.CSV',
                                                 csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-140_s-3072_m-500000.CSV',  csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-160_s-3038_m-500000.CSV',   csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-180_s-3028_m-500000.CSV',  csv_ken_free + 'COIN_018.2_central_c-budgeting_i-1.0_f-200_s-3022_m-500000.CSV']
    f_name_categories['free_abate_budgeting_s'] = [csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-1.0_f-0.0_s-3008_m-100000.CSV',        csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-10.0_s-3012_m-100000.CSV',   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-20.0_s-3016_m-100000.CSV',    csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-30.0_s-3014_m-100000.CSV',
                                                   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-40.0_s-3008_m-100000.CSV',    csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-50.0_s-3009_m-100000.CSV',   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-60.0_s-3010_m-100000.CSV',    csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-70.0_s-3008_m-100000.CSV',
                                                   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-80.0_s-3008_m-100000.CSV',    csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-90.0_s-3012_m-100000.CSV',   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-100.0_s-3008_m-100000.CSV',   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-120.0_s-3015_m-100000.CSV',
                                                   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-140.0_s-3009_m-100000.CSV',   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-160.0_s-3013_m-100000.CSV',  csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-180.0_s-3009_m-100000.CSV',   csv_lei_path + 'COIN_020_valueOfCO2_p-0_c-budgeting_s_i-1.0_f-200.0_s-3010_m-100000.CSV']

    #### (5) 1-tech p1 and p2
    # find_best('1-tech', csv_lei_path)
    f_name_categories['1-tech_balancing_p0'] = csv_ken_path + 'COIN_018_central_c-balancing_i-10.0_s-67_m-100000.CSV'
    f_name_categories['1-tech_balancing_p1'] = csv_lei_path + 'COIN_020_central_p-1_c-balancing_i-10.0_f-0.0_s-3009_m-100000.CSV'
    f_name_categories['1-tech_balancing_p2'] = csv_lei_path + 'COIN_020_central_p-2_c-balancing_i-10.0_f-0.0_s-3008_m-100000.CSV'
    f_name_categories['1-tech_budgeting_p0'] = csv_ken_path + 'COIN_018_central_c-budgeting_i-10.0_s-16_m-100000.CSV'
    f_name_categories['1-tech_budgeting_p1'] = csv_lei_path + 'COIN_020_central_p-1_c-budgeting_i-10.0_f-0.0_s-3008_m-100000.CSV'
    f_name_categories['1-tech_budgeting_p2'] = csv_lei_path + 'COIN_020_central_p-2_c-budgeting_i-10.0_f-0.0_s-3015_m-100000.CSV'
    f_name_categories['1-tech_budgeting_s_p0'] = csv_lei_path + 'COIN_020_central_p-0_c-budgeting_s_i-10.0_f-0.0_s-3010_m-100000.CSV'
    f_name_categories['1-tech_budgeting_s_p1'] = csv_lei_path + 'COIN_020_central_p-1_c-budgeting_s_i-10.0_f-0.0_s-3011_m-100000.CSV'
    f_name_categories['1-tech_budgeting_s_p2'] = csv_lei_path + 'COIN_020_central_p-2_c-budgeting_s_i-10.0_f-0.0_s-3011_m-100000.CSV'

    f_name_categories['free_abate_balancing']

    return f_name_categories



# # ---------------------------   Find the best one case  --------------------------- #



def get_csv_content(file_name):
    with open(file_name, 'rU') as f_open:
        f_read  =  csv.reader(f_open, delimiter=',')
        var_table  =  np.array(list(f_read))

    info_parameter  =  list([])
    for idx in range(len(var_table)):
        info_parameter.append(  str(var_table[idx][0])  )
    return var_table, info_parameter


def get_var_from_table(table, var_list, info_parameter):
    outputs = {}
    for var_idx in var_list:
        if var_idx == 'tot_cost_NoSaving':
            idx1 = info_parameter.index('abateCost')
            var1 = np.array(table[idx1][1:]).astype(float)
            idx2 = info_parameter.index('damages')
            var2 = np.array(table[idx2][1:]).astype(float)
            outputs[var_idx] = var1 + var2
        else:
            idx = info_parameter.index(var_idx)
            var = np.array(table[idx][1:]).astype(float)
            outputs[var_idx] = var
    return outputs


def learning_subsidy(table_in):
    # Term1: The gross production allocated to the new technology
    tlist = table_in['tlist']
    eGross = table_in['eGross']
    mcAbateTech_0 = table_in['mcAbateTech_0']
    # rr = np.exp(-0.03 * tlist)  # prstpVal = 0.03
    abateCostTech_1 = table_in['abateCostTech_1']

    # Find the threshold of miu_1
    miuTech_0 = table_in['miuTech_0']; pBackTime_0 = table_in['pBackTime_0']
    miuTech_1 = table_in['miuTech_1']; pBackTime_1 = table_in['pBackTime_1']
    miuTech_1_threshold = 2 * pBackTime_0 * miuTech_0 / pBackTime_1 - 1
    miuTech_1_threshold[miuTech_1_threshold<0] = 0
    miuTech_1_threshold[miuTech_1_threshold>miuTech_1] = miuTech_1[miuTech_1_threshold>miuTech_1]
    additional_fraction = miuTech_1 - miuTech_1_threshold
    ### allocation to the new technology that is available at a cost no greater than the marginal cost
    abateCostTech_1_less_miu_threshold = eGross * pBackTime_1 * (0.5 * miuTech_1_threshold + 0.5 * miuTech_1_threshold**2 / 2) 
    ### additional deployment fraction times the marginal cost of COIN abatement
    abateCostTech_0_if =  eGross * additional_fraction * mcAbateTech_0
    # Sum up:
    learning_subsidy_results = (abateCostTech_1 - abateCostTech_1_less_miu_threshold - abateCostTech_0_if) * 100 # 100 is the scale

    # ### Check non-mono behavior
    # # print ()
    # # print ()
    # # print (learning_subsidy_results[24:29]) 
    # # print () 
    # # print (abateCostTech_1[24:29]) 
    # # print (abateCostTech_1_less_miu_threshold[24:29]) 
    # # print (abateCostTech_0_if[24:29]) 
    # # print ()
    # # print (miuTech_1_threshold[24:29])
    # print (miuTech_1_threshold[20:80])
    # import matplotlib.pyplot as plt 
    # plt.plot(tlist, abateCostTech_1*100, color='black')
    # plt.plot(tlist, abateCostTech_1_less_miu_threshold*100, color='red')
    # plt.plot(tlist, abateCostTech_0_if*100, color='blue')
    # plt.plot(tlist, learning_subsidy_results, color='green')
    # plt.xlim(0, 150)
    # # plt.ylim(0, 0.5)
    # # plt.xlim(20, 30)
    # plt.ylim(0, 5)
    # plt.show()
    # plt.clf() 
    # stop 

    return learning_subsidy_results



if __name__ == '__main__':
    print ()

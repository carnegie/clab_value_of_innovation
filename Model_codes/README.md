Updated by Lei Duan on August 11, 2023


(1) This folder includes codes of the COIN model that were used for our paper. The latest updates and more details about COIN can be found at: https://github.com/carnegie/COIN.  


(2) The optimization of COIN is written based on MIDACO, which is a commercial solver for numerical optimization problems. People who intend to run COIN should install the MIDACO solver first, put corresponding configuration files under the same folder, and change the "MIDACO_KEY" parameter in COIN_diffeqs.py. 

MIDACO solver can be obtained here: http://www.midaco-solver.com/.


(3) All cases involved in our analysis are summarized in run_COIN_020_caseSummary.py. When running the model, one should consider to run each scenario separately. 



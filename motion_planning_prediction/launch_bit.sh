rm -rf result_files/*.csv
python prediction_simulation_2D.py 1 1 64 MPNET | tee logfile result_files/mpnet_2d_pred.csv 
python prediction_simulation_2D.py 1 1 64 BIT | tee logfile result_files/bit_2d_pred.csv 
python prediction_simulation_2D.py 1 1 64 GNN | tee logfile result_files/gnn_2d_pred.csv 

python CSP_simulation_2D.py MPNET | tee logfile result_files/mpnet_2d_csp.csv 
python CSP_simulation_2D.py BIT | tee logfile result_files/bit_2d_csp.csv 
python CSP_simulation_2D.py GNN | tee logfile result_files/gnn_2d_csp.csv 

python prediction_simulation_nDOF.py 1 0.125 8 MPNET | tee logfile result_files/mpnet_nDOF_pred.csv 
python prediction_simulation_nDOF.py 1 0.125 8 BIT | tee logfile result_files/bit_nDOF_pred.csv 
python prediction_simulation_nDOF.py 1 0.125 8 GNN | tee logfile result_files/gnn_nDOF_pred.csv 

python CSP_simulation_nDOF.py MPNET | tee logfile result_files/mpnet_nDOF_csp.csv 
python CSP_simulation_nDOF.py BIT | tee logfile result_files/bit_nDOF_csp.csv 
python CSP_simulation_nDOF.py GNN | tee logfile result_files/gnn_nDOF_csp.csv 

cd result_files
paste -d " " gnn_2d_csp.csv gnn_2d_pred.csv > gnn_2d.csv
paste -d " " bit_2d_csp.csv bit_2d_pred.csv > bit_2d.csv
paste -d " " mpnet_2d_csp.csv mpnet_2d_pred.csv > mpnet_2d.csv

paste -d " " gnn_nDOF_csp.csv gnn_nDOF_pred.csv > gnn_7d.csv
paste -d " " bit_nDOF_csp.csv bit_nDOF_pred.csv > bit_7d.csv
paste -d " " mpnet_nDOF_csp.csv mpnet_nDOF_pred.csv > mpnet_7d.csv
cd ../




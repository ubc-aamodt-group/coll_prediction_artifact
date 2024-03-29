rm -rf result_files/perf_data.csv
python perf_csp_simulation_mpnet.py 1 >> result_files/perf_data.csv
python perf_prediction_simulation_mpnet.py 1 0.125 1 >> result_files/perf_data.csv
python perf_csp_simulation_mpnet.py 4 >> result_files/perf_data.csv
python perf_prediction_simulation_mpnet.py 1 0.125 4 >> result_files/perf_data.csv
python perf_csp_simulation_mpnet.py 6 >> result_files/perf_data.csv
python perf_prediction_simulation_mpnet.py 1 0.125 6 >> result_files/perf_data.csv
rm -rf result_files/coord_mid.csv
rm -rf result_files/coord_low.csv
rm -rf result_files/coord_high.csv
python coord_hashing.py low 4 -1 1 >> result_files/coord_low.csv
python coord_hashing.py low 4 2 1 >> result_files/coord_low.csv
python coord_hashing.py low 4 1 1 >> result_files/coord_low.csv
python coord_hashing.py low 4 0.5 1 >> result_files/coord_low.csv
python coord_hashing.py low 4 0.125 1 >> result_files/coord_low.csv
python coord_hashing.py low 4 0.03125 1 >> result_files/coord_low.csv
python coord_hashing.py low 4 0 1 >> result_files/coord_low.csv

python coord_hashing.py mid 4 -1 1 >> result_files/coord_mid.csv
python coord_hashing.py mid 4 2 1 >> result_files/coord_mid.csv
python coord_hashing.py mid 4 1 1 >> result_files/coord_mid.csv
python coord_hashing.py mid 4 0.5 1 >> result_files/coord_mid.csv
python coord_hashing.py mid 4 0.125 1 >> result_files/coord_mid.csv
python coord_hashing.py mid 4 0.03125 1 >> result_files/coord_mid.csv
python coord_hashing.py mid 4 0 1 >> result_files/coord_mid.csv

python coord_hashing.py high 4 -1 1 >> result_files/coord_high.csv
python coord_hashing.py high 4 2 1 >> result_files/coord_high.csv
python coord_hashing.py high 4 1 1 >> result_files/coord_high.csv
python coord_hashing.py high 4 0.5 1 >> result_files/coord_high.csv
python coord_hashing.py high 4 0.125 1 >> result_files/coord_high.csv
python coord_hashing.py high 4 0.03125 1 >> result_files/coord_high.csv
python coord_hashing.py high 4 0 1 >> result_files/coord_high.csv
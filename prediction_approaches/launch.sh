rm -rf result_files/result_low.csv
rm -rf result_files/result_high.csv
python pose_hashing.py low 2 pose >> result_files/result_low.csv
python pose_hashing.py low 3 pose >> result_files/result_low.csv
python pose_hashing.py low 2 posepart >> result_files/result_low.csv
python pose_hashing.py low 2 posefold >> result_files/result_low.csv
python pose_hashing.py low 3 posefold >> result_files/result_low.csv
python enpose_hashing_cpu.py low 2 pose >> result_files/result_low.csv
python enpose_hashing_cpu.py low 3 pose >> result_files/result_low.csv
python encoord_hashing.py low 5 0.25 1 2 >> result_files/result_low.csv
python encoord_hashing.py low 3 0.25 1 4 >> result_files/result_low.csv
python coord_hashing.py low 3 0.25 1 >> result_files/result_low.csv
python coord_hashing.py low 4 0.25 1 >> result_files/result_low.csv

python pose_hashing.py high 2 pose >> result_files/result_high.csv
python pose_hashing.py high 3 pose >> result_files/result_high.csv
python pose_hashing.py high 2 posepart >> result_files/result_high.csv
python pose_hashing.py high 2 posefold >> result_files/result_high.csv
python pose_hashing.py high 3 posefold >> result_files/result_high.csv
python enpose_hashing_cpu.py high 2 pose >> result_files/result_high.csv
python enpose_hashing_cpu.py high 3 pose >> result_files/result_high.csv
python encoord_hashing.py high 5 0.25 1 2 >> result_files/result_high.csv
python encoord_hashing.py high 3 0.25 1 4 >> result_files/result_high.csv
python coord_hashing.py high 3 1 1 >> result_files/result_high.csv
python coord_hashing.py high 4 1 1 >> result_files/result_high.csv
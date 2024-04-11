# MPAccel_sim

This repository contains code for the work on "Accelerated Collision-Prediction for Autonomous Robots" (**ISCA Paper ID: **).


#### Environment setup
This code is developed using on Python 3.6.12. 

1. Create a virtual environment and activate with python==3.6.12 (**optional to use virtual environment) 
	``` conda create -n pred_env python==3.6.12```
	
2. Activate the environment
	```conda activate pred_env```
	
3. Install dependencies
	````
	python -m pip install -r requirements.txt
	````
4. Download the required data and files
    ```
    bash download.sh
    ```

 
## Comparison of collision prediction approaches

The experiments required for Figure 9, Figure 13, and Figure 14 can be executed using the following set of scripts. All scripts should take less than 20 minutes. \\
```
cd prediction_approaches
## Run all experiments for Figure 9
bash fig9.sh
## Run all experiments for Figure 13
bash fig13.sh
## Run all experiments for Figure 14
bash fig14.sh
```

## Collision prediction for motion planning (COPU+CDU)

The experiments required for Figure 15 and Figure 16, and results reported in Section 5 can be run using the following commands. 

```
cd  motion_planning_prediction
## Run all experiments for Figure 15
bash fig15.sh 
## Run all experiments for Figure 16
bash fig16.sh 
```

## Trace Generation

We have provided the required trace files for the [comparison of prediction approaches](#markdown-header-comparison-of-collision-prediction-approaches) and for evaluating [collision prediction for different motion planning algorithms](#markdown-header-collision-prediction-for-motion-planning-(copu+cdu)) in the ''trace_files'' folder. In this section, we provide scripts to generate these traces for different robot poses, environmental scenarios, and motion planning algorithms as examples of the trace generation process. 

1. Pose and Coordinate information for comparing prediction approaches:

Comparison of different prediction approaches uses different robot poses in a given environmental scenario (i.e., placement of obstacles). The scripts provided below generate 400 environmental scenarios with 1000 robot poses sampled per environmental scenario. These scripts will store generated traces in  the ''trace_generation/scene_benchmark'' folder, which can be used for the [comparison of prediction approaches](#markdown-header-comparison-of-collision-prediction-approaches) instead of ''trace_files/scene_benchmarks''.  

```
cd trace_generation
conda deactivate
conda create -n new_env python==3.7.0
conda activate new_env
python -m pip install -r requirements.txt
bash launch_pred.sh
```
 
2. Motion trace generation for COPU+CDU:

We provide an example of trace generation for a motion planning algorithm for the evaluation of COPU+CDU using a microarchitectural simulator. We give implementation for BIT*-KUKA motion planning, and a similar approach can be used for other motion planning algorithms. Note that the scripts below were tested on Ubuntu 18.04. 

```
cd trace_generation/bit_planning
conda deactivate
conda create -n myenv python==3.8.17
conda activate myenv
bash install.sh
bash launch_bit_trace.sh
```

The above scripts will generate trace files required for collision prediction simulation using the BIT* motion planning algorithm for the KUKA robot. The above scripts will store generated traces in ''coll_prediction_artifact/trace_generation/logfiles_BIT_link'' folder, which can be used for evaluation [collision prediction for BIT*-KUKA motion planning](#markdown-header-collision-prediction-for-motion-planning-(copu+cdu)) instead of using provided traces in ''coll_prediction_artifact/trace_files/motion_traces/logfiles_BIT_link''. 

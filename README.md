# MPAccel_sim

This repository contains code for the work on "Accelerated Collision-Prediction for Autonomous Robots" (**ISCA Paper ID: **).


#### Environment setup
This code is developed using on Python 3.6.12. 

1. Create a virtual environment and activate with python==3.6.12 (**optional to use virtual environment) 
	``` conda create -n pred_env python==3.6.12```
	
2. Activate the environment
	```Conda activate pred_env```
	
3. Install dependencies
	````
	python -m pip install -r requirements.txt
	````
4. Download required data and files
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

## Collision prediction for motion planning (COPU+CDU):

The experiments required for Figure 15 and Figure 16, and results reported in Section 5 can be run using the following commands. 

```
cd  motion_planning_prediction
## Run all experiments for Figure 15
bash fig15.sh 
## Run all experiments for Figure 16
bash fig16.sh 
```

## Trace Generation


1. Pose and Coordinate information for comparing prediction approaches: 

```
cd trace_generation
conda create -n new_env python==3.7.0
conda activate new_env
python -m pip install -r requirements.txt
bash launch_pred.sh
```
The above script will store generated traces in scene\_benchmark folder. This folder can be used for evaluation outlined in Section~\ref{sec:comp_art}. 
 
2. Motion trace generation for COPU+CDU: 
We provide an example of trace generation for a motion planning algorithm for evaluation of COPU+CDU using a microarchitectural simulator. We give implementation for BIT*-KUKA motion planning, and similar approach can be used for other motion planning algorithms. These scripts were tested on Ubuntu 18.04.

```
cd trace_generation/bit_planning
conda deactivate
conda create -n myenv python==3.8.17
conda activate myenv
python -m pip install -r requirements.txt
bash launch_bit_trace.sh
```

Above scripts will generate trace files required for collision prediction simulation using BIT* motion planning algorithm for KUKA robot. 

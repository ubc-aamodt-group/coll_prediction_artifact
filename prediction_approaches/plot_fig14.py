
import random
from tqdm import tqdm
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
import pandas as pd
import sys
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

font = {
    'family' : 'Times New Roman',
    'weight' : 'normal',
    'size'   : 35,
}

def find_sim_cost(R,C,A,N):
    all_runs=0
    for ex in tqdm(range(0,10000)):
        pred=[]
        non_pred=[]
        for i in range(0,N):
            if random.random()<=R*C/A:
                pred.append(1)
            else:
                non_pred.append(1)
        coll=0
        runs=0
        for i in pred:
            runs+=1
            if random.random()<=A:
                coll=1
                break
        if coll==0:
            for i in non_pred:
                runs+=1
                if random.random()<=(R*(1-C/A)):
                    coll=1
                    break
        all_runs+=runs
    return (all_runs/10000)



dflow = pd.read_csv ("result_files/coord_mid_su.csv",header=None,sep=",")
mid_acc2=dflow[0].tolist()
mid_cov2=dflow[1].tolist()


mid_cost2=[]
width = 1
N=80
R=0.11
for i,j in zip(mid_cov2,mid_acc2):
    sim_cost=find_sim_cost(R,i/100,j/100,N)
    mid_cost2.append(sim_cost)

scale=np.max(mid_cost2)
mid_cost_scale2=[i*100/scale for i in mid_cost2]
print(mid_cost_scale2)
fig = plt.figure(figsize=(16,6))
plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
group=list(range(0,30,5))

ax.bar(group,mid_acc2,width, color="navy",label="Precision (%)")
group= [x +1 for x in group]
ax.bar(group,mid_cov2,width, color="cornflowerblue",label="Recall (%)")
group= [x +1 for x in group]
ax.bar(group,mid_cost_scale2,width, color="tab:orange",label="Compute (%)")
#ax.legend(loc="upper center")
#ax.legend(bbox_to_anchor=(0.1, 1.05),ncol=2)
ax.legend(ncol=2,fontsize=28)
ax.set_xticks([i-1 for i in group]) 
ax.set_xticklabels(["Random","S=0\nU=0","S=1/2\nU=1","S=1\nU=1/2","S=2\nU=1/4","S=4\nU=1/8"], rotation = 0)
ax.set_yticks([0,50,100]) 
ax.set_yticklabels(["0%","50%","100%"], rotation = 0)
ax.axvline(x = 3.5,ymin=0,ymax=1, color = 'gray',lw=0.5)
#ax.set_title("Low obstacles density")
#ax.set_xlabel("Hash code bitwidth")
#ax.set_ylabel("Collision Prediction \n Accuracy/Coverage (%)")

plt.text(1, -26, "Baseline",ha="center",va="top", fontsize=36,color="tab:blue")
plt.text(16, -26, "COORD Collision prediction",ha="center",va="top", fontsize=36,color="tab:blue")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)


plt.savefig('fig14_coord_prediction_mid_upfreq.pdf')
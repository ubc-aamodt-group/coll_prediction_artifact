
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




def find_cost(R,C,A,N):
    expected_random=0
    expected_known=0
    for i in range(1,N+1):
        expected_random+=((1-R)**(i-1))*R*i
    #print(expected_random)
    for i in range(1,int(N*R*C/A)+1):
        expected_known+=((1-A)**(i-1))*A*i
    #if A>0.95:
    #    print(A,expected_known)
    for i in range(1,(N+1)-int(N*R*C/A)):
        expected_known+=((1-R)**(i-1))*R*i*((1-A)**int(N*R*C/A))
    #if A>0.95:
    #    print(A,expected_known,((1-A)**int(N*R*C/A)))
    #for i in range(int(N*R*C/A),N+1):
    #    expected_known+=((1-R)**(i-1))*R
    #print(expected_known)
    return expected_random,expected_known
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



dflow = pd.read_csv ("result_files/coord_low.csv",header=None,sep=",")
low_acc=dflow[0].tolist()
low_cov=dflow[1].tolist()

dflow = pd.read_csv ("result_files/coord_mid.csv",header=None,sep=",")
mid_acc=dflow[0].tolist()
mid_cov=dflow[1].tolist()

dflow = pd.read_csv ("result_files/coord_high.csv",header=None,sep=",")
high_acc=dflow[0].tolist()
high_cov=dflow[1].tolist()

low_cost=[]
mid_cost=[]
high_cost=[]
width = 1
R=0.027
N=80
for i,j in zip(low_cov,low_acc):
    sim_cost=find_sim_cost(R,i/100,j/100,N)
    low_cost.append(sim_cost)
R=0.11
for i,j in zip(mid_cov,mid_acc):
    sim_cost=find_sim_cost(R,i/100,j/100,N)
    mid_cost.append(sim_cost)
R=0.26
for i,j in zip(high_cov,high_acc):
    sim_cost=find_sim_cost(R,i/100,j/100,N)
    high_cost.append(sim_cost)
scale=np.max(low_cost)
low_cost_scale=[i*100/scale for i in low_cost]
scale=np.max(mid_cost)
mid_cost_scale=[i*100/scale for i in mid_cost]
scale=np.max(high_cost)
high_cost_scale=[i*100/scale for i in high_cost]


fig = plt.figure(figsize=(16,7.3))
plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
group=list(range(0,35,5))
print(low_acc)
ax.bar(group,low_acc,width, color="navy",label="Precision (%)")
group= [x +1 for x in group]
ax.bar(group,low_cov,width, color="cornflowerblue",label="Recall (%)")
group= [x +1 for x in group]
ax.bar(group,low_cost_scale,width, color="tab:orange",label="Compute (%)")
#ax.legend(loc="upper center")
ax.legend(bbox_to_anchor=(0.1, 1.05),ncol=2)
ax.set_xticks([i-1 for i in group]) 
ax.set_xticklabels(["Random","S=2","S=1","S=1/2","S=1/8","S=1/32","S=0"], rotation = 0)
ax.set_yticks([0,50,100]) 
ax.set_yticklabels(["0%","50%","100%"], rotation = 0)
ax.axvline(x = 3.5,ymin=0,ymax=1, color = 'gray',lw=0.5)
#ax.set_title("Low obstacles density")
#ax.set_xlabel("Hash code bitwidth")
#ax.set_ylabel("Collision Prediction \n Accuracy/Coverage (%)")

plt.text(1, -20, "Baseline",ha="center",va="top", fontsize=36,color="tab:blue")
plt.text(18, -20, "COORD Collision prediction",ha="center",va="top", fontsize=36,color="tab:blue")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)


plt.savefig('coord_prediction_low_fig13a.pdf')
plt.clf()

fig = plt.figure(figsize=(16,5))
plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
group=list(range(0,35,5))
width = 1
ax.bar(group,mid_acc,width, color="navy",label="Accuracy (%)")
group= [x +1 for x in group]
ax.bar(group,mid_cov,width, color="cornflowerblue",label="Coverage (%)")
group= [x +1 for x in group]
ax.bar(group,mid_cost_scale,width, color="tab:orange",label="Compute (%)")
#ax.legend(loc="upper center")
ax.set_xticks([i-1 for i in group]) 
ax.set_xticklabels(["Random","S=2","S=1","S=1/2","S=1/8","S=1/32","S=0"], rotation = 0)
ax.set_yticks([0,50,100]) 
ax.set_yticklabels(["0%","50%","100%"], rotation = 0)
ax.axvline(x = 3.5,ymin=0,ymax=1, color = 'gray',lw=0.5)
#ax.set_title("Low obstacles density")
#ax.set_xlabel("Hash code bitwidth")
#ax.set_ylabel("Collision Prediction \n Accuracy/Coverage (%)")

plt.text(1, -20, "Baseline",ha="center",va="top", fontsize=36,color="tab:blue")
plt.text(18, -20, "COORD Collision prediction",ha="center",va="top", fontsize=36,color="tab:blue")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)



plt.savefig('coord_prediction_mid_fig13b.pdf')
plt.clf()

fig = plt.figure(figsize=(16,5))
plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
group=list(range(0,35,5))
width = 1
ax.bar(group,high_acc,width, color="navy",label="Accuracy (%)")
group= [x +1 for x in group]
ax.bar(group,high_cov,width, color="cornflowerblue",label="Coverage (%)")
group= [x +1 for x in group]
ax.bar(group,high_cost_scale,width, color="tab:orange",label="Compute (%)")
#ax.legend(loc="upper center")
ax.set_xticks([i-1 for i in group]) 
ax.set_xticklabels(["Random","S=2","S=1","S=1/2","S=1/8","S=1/32","S=0"], rotation = 0)
ax.set_yticks([0,50,100]) 
ax.set_yticklabels(["0%","50%","100%"], rotation = 0)
ax.axvline(x = 3.5,ymin=0,ymax=1, color = 'gray',lw=0.5)
#ax.set_title("Low obstacles density")
#ax.set_xlabel("Hash code bitwidth")
#ax.set_ylabel("Collision Prediction \n Accuracy/Coverage (%)")
plt.text(1, -20, "Baseline",ha="center",va="top", fontsize=36,color="tab:blue")
plt.text(18, -20, "COORD Collision prediction",ha="center",va="top", fontsize=36,color="tab:blue")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)



plt.savefig('coord_prediction_high_fig13c.pdf')
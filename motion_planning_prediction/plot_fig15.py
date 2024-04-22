import pandas as pd
import pickle


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

width=1
name=sys.argv[1]
dfnp = pd.read_csv ("result_files/"+name+".csv",header=None,sep=" ")
parallel_q=[]
serial_q=[]
cpu_q=[]
oracle_q=[]

dfnp=dfnp.sort_values(1)
#print(dfnp,dfnp.iloc[0,1])
num_entry=len(dfnp.axes[0])
bins=5
binsize=math.ceil(num_entry/bins)
#print(num_entry,bins,binsize)
for i in range(0,len(dfnp.axes[0]),binsize):
    parallel_q.append([])
    serial_q.append([])
    cpu_q.append([])
    oracle_q.append([])
    for j in range(i,min(i+binsize,num_entry)):        
        parallel_q[-1].append(dfnp.iloc[j,0])
        serial_q[-1].append(dfnp.iloc[j,1])
        cpu_q[-1].append(dfnp.iloc[j,2])
        oracle_q[-1].append(dfnp.iloc[j,3])
    
#print(parallel_q[0],oracle_q[0])
fig = plt.figure(figsize=(16,5))
plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
group=list(range(0,bins*4,4))
parallel_f=[]
cpu_f=[]
oracle_f=[]
print(np.mean(dfnp[0]),np.mean(dfnp[2]),(np.sum(dfnp[0])-np.sum(dfnp[2]))/np.sum(dfnp[0]))

print("Average computation reduction compared to CSP:  ",100*(np.sum(dfnp[0])-np.sum(dfnp[2]))/np.sum(dfnp[0]))
scale=np.mean(parallel_q[0])
for i,j,k in zip(parallel_q,cpu_q,oracle_q):
    parallel_f.append(np.mean(i)/scale)
    cpu_f.append(np.mean(j)/scale)
    oracle_f.append(np.mean(k)/scale)
#print(parallel_f,cpu_f,oracle_f,group)
ax.bar(group,parallel_f, width,color="tab:orange",label="CSP")
group= [x +1 for x in group]
ax.bar(group,cpu_f,width, color="tab:blue",label="CSP+CP")
group= [x +1 for x in group]
ax.bar(group,oracle_f,width, color="tab:gray",label="Oracle")
##print("g5",(parallel_f[4]-oracle_f[4])/parallel_f[4],(parallel_f[4]-cpu_f[4])/parallel_f[4])

print("Computation reduction compared to CSP For group 5 (more cluttered environments): ",100*(parallel_f[4]-cpu_f[4])/parallel_f[4])
#group= [x +1 for x in group]
#ax.bar(group,lows_cost+highs_cost,width, color="tab:orange",label="Compute (%)")
#ax.legend(loc="upper center")
#ax.legend(bbox_to_anchor=(0.1, 1.05),ncol=2)
ax.legend(ncol=2)
ax.set_xticks([i-1 for i in group]) 
lab=[]
for i in range(1,bins+1):
    lab.append("G"+str(i))
ax.set_xticklabels(lab, rotation = 0)
#ax.set_yticks([0,50,100]) 
#ax.set_yticklabels(["0%","50%","100%"], rotation = 0)
#ax.axvline(x = 11,ymin=0,ymax=1, color = 'gray',lw=0.5)
#ax.set_title("Low obstacles density")
ax.set_xlabel("Groups of motion planning queries")
ax.set_ylabel("#Collision Queries\n(Normalized)")

#plt.text(5, -24, "Low speed (10-30km/h)",ha="center",va="top", fontsize=36,color="tab:blue")
#plt.text(17, -24, "High speed (30-50km/h)",ha="center",va="top", fontsize=36,color="tab:blue")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)


plt.savefig(sys.argv[2]+'_'+name+'.pdf')

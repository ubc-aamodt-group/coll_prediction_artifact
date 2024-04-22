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


fig = plt.figure(figsize=(16,8))

#Single group, parallel, CSP, BRP - this is how it stores data in the Panda file
#multi motion
#sm,npm,cm,bm,np,c,b - t combinations makes sense
dfnp = pd.read_csv ("result_files/perf_data.csv",header=None,sep=" ")
#print(dfnp['mpnet'])
print(dfnp)

ncdu=dfnp[0].to_numpy()
cycles=dfnp[1].to_numpy()
coll=dfnp[2].to_numpy()
#utlization=[]
#for i,j,k in zip(cycles,coll,ncdu):
    
#utlilzation = cycles/(coll*40*ncdu)
utlization=( coll*40/(cycles*ncdu))

oocd_area=0.172
oocd_power=41.04
obb_area=0.054
obb_power= 30
copu_area=0.0465 
copu_power=4+11/4

#500 MHz frequency
throughpout=500000000/cycles

total_power= (utlization*ncdu*oocd_power+obb_power+[0,copu_power,0,copu_power,0,copu_power])/1000
total_area= (ncdu*oocd_area+obb_area+[0,copu_area,0,copu_area,0,copu_area])

perfw = throughpout/total_power
perfa = throughpout/total_area

perfw_norm = perfw/perfw[0]
perfa_norm = perfa/perfa[0]
tput_norm = throughpout/throughpout[0]
runtime_norm = 1/tput_norm

#print(perfa_norm,perfw_norm)
#print(total_power,total_area)

plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
group=list(range(1,7))
#group=list(range(0,bins*4,4))



ax.plot(group,perfw_norm,color="tab:orange",label="Perf/W",linewidth=0,marker="<",markersize=20)
ax.plot(group,perfa_norm,color="tab:blue",label="Perf/mm2",linewidth=0,marker="*",markersize=20)
ax.plot(group,runtime_norm,color="tab:green",label="Runtime",linewidth=0,marker="o",markersize=20)

ax.legend(ncol=3)
ax.set_xticks([i for i in group]) 
lab=["Baseline.1","COPU.1","Baseline.4","COPU.4","Baseline.6","COPU.6"]

ax.set_xticklabels(lab, rotation = 20)

#ax.set_yticklabels(["15","20","25"])
#ax.set_yticks([0,50,100]) 
#ax.set_yticklabels(["0%","50%","100%"], rotation = 0)
#ax.axvline(x = 11,ymin=0,ymax=1, color = 'gray',lw=0.5)
#ax.set_title("Low obstacles density")
ax.set_ylabel("Perf/W or Perf/mm2 \n or Runtime (Normalized)")
ax.set_xlabel("Configurations")
ax.set_ylim(0,2.5)

#plt.show()
#plt.text(5, -24, "Low speed (10-30km/h)",ha="center",va="top", fontsize=36,color="tab:blue")
#plt.text(17, -24, "High speed (30-50km/h)",ha="center",va="top", fontsize=36,color="tab:blue")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
#plt.show()

plt.savefig('perf_area_plot.pdf')

print("perf/W increase for COPU.1, COPU.4, and COPU.6: ",perfw_norm[1]/perfw_norm[0],perfw_norm[3]/perfw_norm[2],perfw_norm[5]/perfw_norm[4])

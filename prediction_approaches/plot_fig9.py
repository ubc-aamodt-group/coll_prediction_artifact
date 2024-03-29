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
plt.rc('font', **font)
width = 1

dflow = pd.read_csv ("result_files/result_low.csv",header=None,sep=",")
accuracy_low=dflow[0].tolist()
coverage_low=dflow[1].tolist()

dfmed = pd.read_csv ("result_files/result_high.csv",header=None,sep=",")
accuracy_med=dfmed[0].tolist()
coverage_med=dfmed[1].tolist()

print(accuracy_low,coverage_low,accuracy_med,coverage_med)
#accuracy_low=[13.68,50,60.95,6.09,7.35,8.7,9.05,71.18,77.35]
#coverage_low=[2.35,0.07,9.4,35,6.76,0.81,2.17,34.56,47.15]
#accuracy_med=[52.42,67.11,76.53,42.96,31.2,43.76,38.36,83.69,83.17]
#coverage_med=[8.33,0.19,56.38,10.04,12.73,17.7,14.14,63.31,76.91]


hashwidth=[12,18,6,6,9,8,12,10,12,9,12]


ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()
#group=[1,2,4,8,16,32,64]
grouplabel=["POSE\n12","POSE\n18","POSE+fold\n6","POSE+fold\n9","ENPOSE\n8","ENPOSE\n12","ENCOORD\n10","ENCOORD\n12","COORD\n9","COORD\n12"]
group=list(range(0,33,3))

ax.bar(group,accuracy_low,width, color="navy",label="Precision")
group= [x +1 for x in group]
ax.bar(group,coverage_low,width, color="cornflowerblue",label="Recall")
ax.legend(loc="upper center")
ax.set_xticks([i-0.5 for i in group]) 
ax.set_xticklabels(hashwidth, rotation = 0)
#ax.set_xlabel("Hash code bitwidth")
ax.set_ylabel("Collision Prediction \n Precision/Recall (%)")
plt.text(2, -13, "POSE",ha="center",va="top")
plt.text(6.5, -13, "POSE\npart",ha="center",va="top")
plt.text(11, -13, "POSE+fold",ha="center",va="top")
plt.text(17, -13, "ENPOSE",ha="center",va="top")
plt.text(23, -13, "ENCOORD",ha="center",va="top")
plt.text(29, -13, "COORD",ha="center",va="top")
ax.axvline(x = 5,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 8,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 14,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 20,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 26,ymin=-15,ymax=100, color = 'gray',lw=0.5)

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('hash_functions_low_fig9a.pdf')

fig = plt.figure(figsize=(16,8))
plt.rc('font', **font)  
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()
#group=[1,2,4,8,16,32,64]
grouplabel=["POSE\n12","POSE\n18","POSE+fold\n6","POSE+fold\n9","ENPOSE\n8","ENPOSE\n12","ENCOORD\n10","ENCOORD\n12","COORD\n9","COORD\n12"]
group=list(range(0,33,3))

ax.bar(group,accuracy_med,width, color="navy",label="Precision")
group= [x +1 for x in group]
ax.bar(group,coverage_med,width, color="cornflowerblue",label="Recall")
ax.legend(loc="upper center")
ax.set_xticks([i-0.5 for i in group]) 
ax.set_xticklabels(hashwidth, rotation = 0)
#ax.set_xlabel("Hash code bitwidth")
ax.set_ylabel("Collision Prediction \n Precision/Recall (%)")
plt.text(2, -13, "POSE",ha="center",va="top")
plt.text(6.5, -13, "POSE\npart",ha="center",va="top")
plt.text(11, -13, "POSE+fold",ha="center",va="top")
plt.text(17, -13, "ENPOSE",ha="center",va="top")
plt.text(23, -13, "ENCOORD",ha="center",va="top")
plt.text(29, -13, "COORD",ha="center",va="top")
ax.axvline(x = 5,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 8,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 14,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 20,ymin=-15,ymax=100, color = 'gray',lw=0.5)
ax.axvline(x = 26,ymin=-15,ymax=100, color = 'gray',lw=0.5)

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('hash_functions_high_fig9b.pdf')
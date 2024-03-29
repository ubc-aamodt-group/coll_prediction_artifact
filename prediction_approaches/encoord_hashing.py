import sys, os, argparse

import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import pickle
import pandas as pd


def plot(code,ytest,name):
    principalComponents=code.data.cpu().numpy()
    #print(principalComponents)
    coll=[]
    collfree=[]
    for i in range(0,len(ytest)):
        if ytest[i]>0.5:
            collfree.append(principalComponents[i])
        else:
            coll.append(principalComponents[i])
    coll1=(np.array(coll))
    collfree1=(np.array(collfree))
    plt.scatter(collfree1[:,0], collfree1[:,1],label="Collision free",color="blue",alpha=0.3)
    plt.scatter(coll1[:,0], coll1[:,1],color="red",label="Colliding",alpha=0.3)
    plt.savefig(name)
    plt.clf()
    plt.close()



consider_dir=False
# distributing the dataset into two components X and Y


binnumber=2**int(sys.argv[2])
intervalsize=2.24/binnumber
bins=np.zeros(binnumber)
start=-1.12
for i in range(0,binnumber):
    bins[i]=start
    start+=intervalsize

all_onezero=0
all_zerozero=0
all_total=0
all_total_colliding=0  # len(label_pred)-np.sum(label_pred)
globalcolldict={}
colldict={}
#print("Total colliding,zerozero,onezero,random_baseline,Prediction_accuracy,Fraction_predicted,link_colliding,link_zerozero,link_onezero")
for benchid in range(0,100):
    benchidstr=str(benchid)
    if sys.argv[1]=="low":
       f=open("../trace_files/scene_benchmarks/moving_1030_10_low/obstacles_"+benchidstr+"_coord.pkl","rb")
       f1=open("../trace_files/scene_benchmarks/low_obstacle_encord/encodecoord_"+sys.argv[5]+"_"+benchidstr+".pkl","rb")
    elif sys.argv[1]=="mid":
       f=open("../trace_files/scene_benchmarks/moving_1030_10_mid/obstacles_"+benchidstr+"_coord.pkl","rb")
       f1=open("../trace_files/scene_benchmarks/low_obstacle_encord/encodecoord_"+sys.argv[5]+"_"+benchidstr+".pkl","rb")
    else:
        f=open("../trace_files/scene_benchmarks/moving_1030_10_high/obstacles_"+benchidstr+"_coord.pkl","rb")
        f1=open("../trace_files/scene_benchmarks/high_obstacle_encord/encodecoord_"+sys.argv[5]+"_"+benchidstr+".pkl","rb")

    xtest_pred,dirr_pred,label_pred=pickle.load(f)
    code=pickle.load(f1)
    f.close()
    f1.close()
    code_pred_quant=np.digitize(code,bins,right=True)
    #print(len(code_pred_quant))
    colldict={}

    bitsize=len(code_pred_quant[0])
    prediction_true=0
    onezero=0
    zerozero=0
    zeroone=0
    total_colliding=0  # len(label_pred)-np.sum(label_pred)

    link_colliding=0
    link_zerozero=0
    link_onezero=0
    all_total+=len(code_pred_quant)
    for bini in range(0,len(code_pred_quant),7):
        #if bini>=2800:
        #   break
        predicted=1
        true_ans=1
        for i in range(bini,bini+7):
            keyy=""
            for j in range(0,bitsize):
                if code_pred_quant[i,j]<10:
                    keyy=keyy+"0"
                keyy=keyy+str(code_pred_quant[i,j])
            if consider_dir:
                keyy=keyy+dirr_pred[i]
            #print(keyy,predicted)
            if keyy in colldict:
                #if colldict[keyy][0]>0:#colldict[keyy][1]:
                if colldict[keyy][0]>(float(sys.argv[3])*colldict[keyy][1]):#colldict[keyy][1]:
                    #print(colldict[keyy],keyy)
                    predicted=0
                    if label_pred[i]>0.5:
                        link_onezero+=1
                ## for continual
                if (label_pred[i]>0.5 and random.random()<=float(sys.argv[4])) or label_pred[i]<0.5: 
                    colldict[keyy][int(label_pred[i])]+=1
            else:
                if (label_pred[i]>0.5 and random.random()<=float(sys.argv[4])) or label_pred[i]<0.5: 
                    colldict[keyy]=[0,0]
                    colldict[keyy][int(label_pred[i])]+=1
            if label_pred[i]<0.5:
                true_ans=0
                link_colliding+=1
                if predicted==0:
                    link_zerozero+=1
                    break
        #print(keyy,predicted)
        if true_ans==0 and predicted==0:
            zerozero+=1
            all_zerozero+=1
        elif true_ans==1 and predicted==0:
            onezero+=1
            all_onezero+=1
            #print(colldict[keyy])
        elif true_ans==0 and predicted==1:
            zeroone+=1
        if true_ans==0:
            total_colliding+=1
            all_total_colliding+=1
    if total_colliding==0 or zerozero==0:
        continue

print("%.2f,%.2f"%(all_zerozero*100/(all_zerozero+all_onezero),all_zerozero*100/all_total_colliding))



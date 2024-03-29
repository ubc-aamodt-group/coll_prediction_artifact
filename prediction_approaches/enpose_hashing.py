import sys, os, argparse

import numpy as np
import matplotlib.pyplot as plt

import random
from tqdm import tqdm
import pickle
import pandas as pd

#sys.path.insert(1, '..//')
import models_new as hopenet
model = hopenet.ResNet(num_classes=6,num_bits=4)
model.load_state_dict(torch.load("../trace_files/model_4_32768.pkl"))
model.eval()

model.cuda()

##binary code
fourbin={4:{0:"00",1:"00",2:"01",3:"10",4:"11"},8:{0:"000",1:"000",2:"001",3:"010",4:"011",5:"100",6:"101",7:"110",8:"111"},16:{1:"0000",2:"0001",3:"0010",4:"0011",5:"0100",6:"0101",7:"0110",8:"0111",9:"1000",10:"1001",11:"1010",12:"1011",13:"1100",14:"1101",15:"1110",16:"1111"}}
fourgray={4:{1:"00",2:"01",3:"11",4:"10"},8:{1:"000",2:"001",3:"011",4:"010",5:"110",6:"111",7:"101",8:"100"},16:{1:"0000",2:"0001",3:"0011",4:"0010",5:"0110",6:"0111",7:"0101",8:"0100",9:"1100",10:"1101",11:"1111",12:"1110",13:"1010",14:"1011",15:"1001",16:"1000"}}
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

def dectobin(num,bits):
    an=""
    n=num
    for i in range(0,bits):
        an=str(int(n%2))+an
        n=int(n/2)
    return an
def return_key(code,binsize):
    codefun=fourbin
    #codefun=fourgray
    bitsize=len(code)
    keyy=""
    #print(code)
    for j in range(0,bitsize):
    #for j in range(0,2):
        #print(int(code[j]))
        keyy=keyy+fourbin[binsize][int(code[j])]
        #print(code[j],fourbin[binsize][int(code[j])])
    return keyy

def return_key_partial(code,binsize):
    codefun=fourbin
    #codefun=fourgray
    bitsize=len(code)
    keyy=""
    #print(code)
    #for j in range(0,bitsize):
    for j in range(0,2):
        #print(int(code[j]))
        keyy=keyy+fourbin[binsize][int(code[j])]
        #print(code[j],fourbin[binsize][int(code[j])])
    return keyy

def fold(s1,s2):
    res=[(ord(a) ^ ord(b)) for a, b in zip(s1, s2)]
    an=""
    for i in res:
        an+=str(i)
    return an
def return_key_fold(code,binsize):
    codefun=fourbin
    #codefun=fourgray
    bitsize=len(code)
    keyyh=""
    keyyl=""
    return fold(fourbin[binsize][int(code[0])],fourbin[binsize][int(code[1])])+ fold(fourbin[binsize][int(code[2])],fourbin[binsize][int(code[3])])+ fold(fourbin[binsize][int(code[4])],fourbin[binsize][int(code[5])])

def return_key_fold_old(code,binsize):
    codefun=fourbin
    #codefun=fourgray
    bitsize=len(code)
    keyyh=""
    keyyl=""
    for j in range(0,int(bitsize/2)):
        keyyh=keyyh+fourbin[binsize][int(code[j])]
    for j in range(int(bitsize/2),bitsize):
        keyyl=keyyl+fourbin[binsize][int(code[j])]
        #print(code[j],fourbin[binsize][int(code[j])])
    
    return fold(keyyh,keyyl)

    
# distributing the dataset into two components X and Y

binnumber=2**int(sys.argv[2])
intervalsize=4/binnumber
bins=np.zeros(binnumber)
start=-2
for i in range(0,binnumber):
    bins[i]=start
    start+=intervalsize
##Hashing function
if sys.argv[3]=="pose":
    hashing_function=return_key#_fold
elif sys.argv[3]=="posepart":
    hashing_function=return_key_partial#_fold
elif sys.argv[3]=="posefold":
    hashing_function=return_key_fold#_fold
else:
    sys.exit()
all_onezero=0
all_zerozero=0
all_total_colliding=0
colldict={}
total_points=0
for benchid in range(0,100):
    #print(benchid)
    benchidstr=str(benchid)
    if sys.argv[1]=="low":
       f=open("../trace_files/scene_benchmarks/moving_1030_10_low/obstacles_"+benchidstr+"_pose.pkl","rb")
    else:
        f=open("../trace_files/scene_benchmarks/moving_1030_10_high/obstacles_"+benchidstr+"_pose.pkl","rb")
    xtest_pred,label_pred=pickle.load(f)
    if True:
        xtest_pred_temp=np.sin(xtest_pred[:, 1:7])
        code,_=model(torch.tensor(xtest_pred_temp).float().cuda())
        code=code.data.cpu().numpy()
        #print(code[0],code[1])
        code_pred_quant=np.digitize(code,bins,right=True)
        #print(code_pred_quant[0],code_pred_quant[1])

    f.close()
    colldict={}
    ##
    for k,v in colldict.items():
        #print(v,int(colldict[k][0]/2))
        sc0=4
        sc1=sc0
        colldict[k][0]=int(colldict[k][0]/sc0)
        colldict[k][1]=int(colldict[k][1]/sc1)

    ##continual prediction
    onezero=0
    zerozero=0
    zeroone=0
    total_colliding=len(label_pred)-np.sum(label_pred)
    all_total_colliding+=total_colliding
    total_points+=len(label_pred)
    bitsize=len(code_pred_quant[0])
    for i in range(0,len(code_pred_quant)):
        #if i>=400:
        #    break
        predicted=1
        keyy=hashing_function(code_pred_quant[i],binnumber)
        if keyy in colldict:
            if colldict[keyy][0]*4>colldict[keyy][1]:
                predicted=0
            colldict[keyy][int(label_pred[i])]+=1
        else:
            colldict[keyy]=[0,0]
            colldict[keyy][int(label_pred[i])]+=1
        if int(label_pred[i])==0 and predicted==0:
            zerozero+=1
            all_zerozero+=1
        elif int(label_pred[i])==1 and predicted==0:
            onezero+=1
            all_onezero+=1
        elif int(label_pred[i])==0 and predicted==1:
            zeroone+=1
    


#print("Precision:", all_zerozero*100/(all_zerozero+all_onezero), "Recall",all_zerozero*100/all_total_colliding)

print("%.2f,%.2f"%(all_zerozero*100/(all_zerozero+all_onezero),all_zerozero*100/all_total_colliding))
#print("random baseline", total_points,all_total_colliding,all_total_colliding/total_points)

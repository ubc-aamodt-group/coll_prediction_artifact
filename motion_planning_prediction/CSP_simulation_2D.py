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


def reutrn_keyy(code):
    bitsize=len(code)
    keyy=""
    for j in range(0,bitsize):
        if code[j]<10:
            keyy=keyy+"0"
        keyy=keyy+str(code[j])
    return keyy
#training for prediction

consider_dir=False

def csp_rearrange(edge,edgeyarr,groupsize=8):
    #recieves a list of poses in the edge and asnwers for that
    num_steps=len(edge)
    rearr=[edge[-1]]
    rearryarr=[edgeyarr[-1]]
    #for i in [0]:
    for i in [0,4,2,6,1,5,3,7]:
        for j in range(i,num_steps-1,8):
        #for j in range(i,num_steps-1,1):
            rearr.append(edge[j])
            rearryarr.append(edgeyarr[j])
    group=[]
    grouparr=[]
    for pose,posecoll in zip(rearr,rearryarr):
        for link,linkcoll in zip(pose,posecoll):
            group.append(link)
            grouparr.append(linkcoll)
    return group,grouparr

# distributing the dataset into two components X and Y


binnumber=32
intervalsize=2/binnumber
bins=np.zeros(binnumber)
start=-1
for i in range(0,binnumber):
    bins[i]=start
    start+=intervalsize

all_csp=0
all_prediction=0
all_oracle=0
globalcolldict={}
colldict={}
fall_serial=0
fall_parallel=0
fall_prediction=0
fall_oracle=0
qnoncoll_len=56
qcoll_len=8
cycle_check=40
#for benchid in [0,10,11,12,13,14,15,16,17,18,19,1,20,21,22,23,24,25,26,27,28,29,2,30,31,32,33,34,35,36,37,38,39,3,40,41,42,43,44,45,46,47,48,49,4,50,51,52,53,54,55,56,57,58,59,5,60,61,62,63,64,65,66,67,68,69,6,70,71,72,73,74,75,76,77,78,79,7,80,81,82,83,84,85,86,87,88,89,8,90,91,92,93,94,95,96,97,98,99,9]:
benchrange=range(0,201)
if sys.argv[1]=="GNN":
    benchrange=range(1,201)

for benchid in benchrange:
    
    all_parallel=0
    all_prediction=0
    all_oracle=0
    colldict={}
    benchidstr=str(benchid)
    
    if sys.argv[1]=="BIT":
        filename="../trace_files/motion_traces/logfiles_BIT_2D/coord_motiom_"+str(benchid)+".pkl"
    elif sys.argv[1]=="GNN":
        filename="../trace_files/motion_traces/logfiles_GNN_2D/coord_motiom_"+str(benchid)+".pkl"
    elif sys.argv[1]=="MPNET":
        filename="../trace_files/motion_traces/logfiles_MPNET_2D/link_info_1_"+str(benchid)+".pkl"

    try:
        f=open(filename,"rb")
    except:
        continue
    #(edge_link_data,edge_link_coll_data)=pickle.load(f)
    (edge_link_data,edge_link_coll_data)=pickle.load(f, encoding='latin1')
    f.close()
    
    for k,v in colldict.items():
        sc=2
        colldict[k][0]=int(colldict[k][0]/sc)
        colldict[k][1]=int(colldict[k][1]/sc)

    #each entry is a tuple (hash code, and output)
    for edge,edge_coll in zip(edge_link_data,edge_link_coll_data):
        sample_phase=0
        if len(edge_coll)==1:
            sample_phase=0
            #all_sample+=1
        #print(edge_coll)
        cycle=0
        first_two_running=0
        first_two_checked=0
        oocds=[]
        for i in range(0,7):
            #hash code, is feasible, is valid, when free
            oocds.append([0,0,0,0])
        qcoll=[]
        qnoncoll=[]

        if len(edge_coll)==0:
            continue
    
        coll_found=0
        for pose,pose_coll in zip(edge,edge_coll):
            for link,link_coll in zip(pose,pose_coll):
                if link_coll==0:
                    coll_found=1
                    break
        if sample_phase==0:
            if coll_found==1:
                all_oracle+=1
            else:
                all_oracle+=(len(edge_coll))
        
        linklist,linklist_coll=csp_rearrange(edge,edge_coll,groupsize=4)
        #print(linklist_coll,all_oracle)
        coll_found=0
        links_remaining=len(linklist)
        everything_free=0
        while coll_found==0 and everything_free==0:
            #print(cycle,links_remaining,coll_found)
            #cycle
            #update collision tables and schedule from queues
            #print(oocds)
            for oocd_id in range(0,len(oocds)):
                oocd=oocds[oocd_id]
                if oocd[2]==1 and oocd[3]<=cycle:
                    #print(oocd)
                    if sample_phase==0:
                        all_prediction+=1
                    if oocd[1]==0:
                        coll_found=1
                    #print(oocd[0],oocd[1])
                    if oocd[0] in colldict:
                        colldict[oocd[0]][oocd[1]]+=1
                    else:
                        colldict[oocd[0]]=[0,0]
                        colldict[oocd[0]][oocd[1]]+=1
                if oocd[3]<=cycle:
                    if len(qnoncoll)>0:
                        oocds[oocd_id]=[qnoncoll[0][0],qnoncoll[0][1],1,cycle+cycle_check]
                        #print("noncoll",len(qnoncoll),links_remaining,cycle,oocds[oocd_id])
                        del qnoncoll[0]
                    else:
                        oocds[oocd_id]=[0,0,0,0]
            if len(linklist)>0:
                link=linklist[0]
                linkcoll=linklist_coll[0]
                code_quant=np.digitize(link,bins,right=True)
                keyy=reutrn_keyy(code_quant)

                if True:
                    if len(qnoncoll)<qnoncoll_len:
                        qnoncoll.append([keyy,linkcoll])
                        #if keyy=="080811":
                        #    print(qnoncoll)
                        #    print(linklist[0],linklist_coll[0])
                        del linklist[0]
                        del linklist_coll[0]
            links_remaining=len(linklist_coll)
            if links_remaining==0:
                everything_free=1
                for oocd in oocds:
                    #print(oocd)
                    if oocd[3]>cycle:
                        everything_free=0
                if len(qnoncoll)>0:
                    everything_free=0
                if len(qcoll)>0:
                    everything_free=0
            cycle+=1
        #print(all_prediction)
        for oocd_id in range(0,len(oocds)):
            oocd=oocds[oocd_id]
            if oocd[3]>cycle:# and <(cycle+10):
                #print(cycle,oocd[3],((cycle_check-oocd[3]+cycle)/cycle_check))
                all_prediction+=((cycle_check-oocd[3]+cycle)/cycle_check)
        #print(colldict)
        #print(all_prediction)
        #break
        #break
        #print(coll_found,all_serial,all_prediction)
    #for k,v in colldict.items():
    #    print(k,v,"\n")
    #print(benchid,"Overall parallel %d Overall serial %d Overall prediction %d Overall oracle %d"%(all_parallel,all_serial,all_prediction,all_oracle))
    #print(benchid,"%d %d %d %d"%(all_parallel,all_serial,all_prediction,all_oracle)) 
    fall_oracle+=all_oracle
    #fall_parallel+=all_parallel
    fall_prediction+=all_prediction
    print(all_prediction,all_oracle)

#print(fall_prediction,fall_oracle)



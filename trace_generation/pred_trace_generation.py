import klampt
from klampt.plan import cspace,robotplanning
from klampt.io import resource
from klampt.model import collide
import klampt.model
from klampt.model import trajectory
import time
import sys
from klampt import vis
import pickle
from typing import NamedTuple
from collections import namedtuple
import numpy as np
import random
import math
from klampt.model.create import primitives
from klampt import WorldModel,Geometry3D

import numpy as np
def give_RT(x):
    R=[]
    T=[]
    for j in range(0,3):
        for i in range(0,3):
            R.append(x[i][j])
        T.append(x[j][3])
    return (R,T)
def get_obbRT(R,T):
    newR= np.eye(3)
    newT=np.array(T)
    pointer=0
    for j in range(0,3):
        for i in range(0,3):
            newR[i][j]=R[pointer]
            pointer+=1
        #newT[j]=T[j]
    #print(T,newT)
    return newR,newT
def give_dh(d,r,th,al):
    new= np.eye(4)
    new[0,0]=math.cos(th)
    new[0,1]=-1*math.cos(al)*math.sin(th)
    new[0,2]=math.sin(al)*math.sin(th)
    new[0,3]=r*math.cos(th)

    new[1,0]=math.sin(th)
    new[1,1]=1*math.cos(al)*math.cos(th)
    new[1,2]=-1*math.sin(al)*math.cos(th)
    new[1,3]=r*math.sin(th)

    new[2,0]=0
    new[2,1]=math.sin(al)
    new[2,2]=math.cos(al)
    new[2,3]=d
    return new

def get_RT(x):
    R=x[0]
    T=x[1]
    new= np.eye(4)
    pointer=0
    for j in range(0,3):
        for i in range(0,3):
            new[i][j]=R[pointer]
            pointer+=1
        new[j][3]=T[j]
    return new

def transform_point(p,R,T):
    new=np.zeros((3,1))
    #print(p,new,R)
    new[:,0]=p
    newT=np.array(T)
    temp=np.matmul(R,new)
    newT[0]+=temp[0,0]
    newT[1]+=temp[1,0]
    newT[2]+=temp[2,0]
    return newT

def inverse(R):
    x=math.atan(R[1][2]/R[0][2])
    y=math.atan(math.sqrt(R[0][2]**2+R[1][2]**2)/R[2][2])
    z=math.atan(-1*R[2][1]/R[2][0])

    return([(x),(y),(z)])


def get_obbs(world,qbase):
    dh01=give_dh(0.1535,0,0,0)
    dh1e=give_dh(0.08,0,qbase[1],0)


    dh12=give_dh(0.1185,0,qbase[1],-1*math.pi/2)
    dh2e=give_dh(-0.029,0.206,qbase[2],0)

    dh23=give_dh(0.0,0.41,qbase[2],0)
    dh3e=give_dh(0.014,-0.08,-1*math.pi/2+qbase[3],-1*math.pi/2)

    dh34=give_dh(0.01125,0.0,qbase[3],-1*math.pi/2)
    dh4e=give_dh(0.25,0.0,1*math.pi+qbase[4],-0.5)
    dh4e=give_dh(0.25,0.0,qbase[4],0.5)
    dh4e=give_dh(0.207,0.0,qbase[4],0)
    dh4ed=np.matmul(give_dh(0.05,0.0,0,0.61),give_dh(0.0,0.014,-1*math.pi/2,0.0))
    dh45=give_dh(0.207+0.0658,0.00,qbase[4],math.pi+0.9599)

    dh5e=give_dh(-0.028,0.01968,(math.pi/2),0.0)
    dh5ed=give_dh(-0.050,0.01,-qbase[5],0.0)

    dh56=np.matmul(give_dh(-0.028,0.01968,(math.pi/2),0.0),give_dh(0,0,-qbase[5],0) )
    dh6e=np.matmul(give_dh(0,0,-1*math.pi/2,0.9599),give_dh(-0.0658,-0.0343,math.pi/2,0))
    dh6ed=give_dh(-0.055,0,-qbase[6],0)

    fin1e=np.matmul(dh01,dh1e)
    fin2e=np.matmul(dh01,np.matmul(dh12,dh2e))
    fin3e=np.matmul(dh01,np.matmul(dh12,np.matmul(dh23,dh3e)))
    fin4e=np.matmul(dh01,np.matmul(dh12,np.matmul(dh23,np.matmul(dh34,np.matmul(dh4e,dh4ed)))))
    fin5e=np.matmul(dh01,np.matmul(dh12,np.matmul(dh23,np.matmul(dh34,np.matmul(dh45,np.matmul(dh5e,(dh5ed)))))))
    fin6e=np.matmul(dh01,np.matmul(dh12,np.matmul(dh23,np.matmul(dh34,np.matmul(dh45,np.matmul(dh56,np.matmul(dh6e,dh6ed)))))))

    KLAMPT_EXAMPLES="../"
    """Makes a new axis-aligned "shelf" centered at the origin with
    dimensions width x depth x height. Walls have thickness wall_thickness.
    """
    sizelist=[[0.10,0.091,0.16],[0.494,0.083,0.053],[0.25,0.064,0.10],[0.072,0.064,0.096],[0.084,0.066,0.1],[0.092,0.116,0.11],[0.084,0.089,0.1535]]
    dump_list=[]
    namelist=["l1","l2","l3","l4","l5","l6","l0"]
    finlist=[fin1e,fin2e,fin3e,fin4e,fin5e,fin6e]
    #link6 = Geometry3D()
    #link6.loadFile("../data/objects/cube.off")
    s=sizelist[6]
    #link6.scale(s[0], s[1],s[2])
    #link6.translate([s[0]*-0.5, -0.5*s[1] ,0])
    obbc=np.array([0,0,s[2]*0.5])
    obbe=np.array([s[0], s[1],s[2]])
    obbr=np.eye(3)
    newpoint=(transform_point(np.array([s[0], s[1],s[2]]),obbr,obbc))
    direction=np.sign(newpoint-obbc)
    if direction[0]<0:
        direction=direction*-1
    direction=((direction+1)/2)
    dirstring=str(int(direction[1]))+str(int(direction[2]))
    dump_list.append([0,obbc,obbe,obbr,dirstring])
    #shelf = world.makeTerrain(namelist[6])
    #shelf.geometry().set(link6)
    #shelf.appearance().setColor(0.2,0.6,0.3,1.0)


    for i in range(0,6):
        R,T=give_RT(finlist[i])
        
        #print(np.array(R),np.array(T))


        #dump_list.append([index,obb.c,obb.e,obb.R])
        #link6 = Geometry3D()
        #link6.loadFile(KLAMPT_EXAMPLES+"/data/objects/cube.off")
        s=sizelist[i]
        obbr,obbc=get_obbRT(R,T)
        newpoint=(transform_point(np.array([s[0], s[1],s[2]]),obbr,obbc))
        direction=np.sign(newpoint-obbc)
        if direction[0]<0:
            direction=direction*-1
        direction=((direction+1)/2)
        dirstring=str(int(direction[1]))+str(int(direction[2]))
        obbe=np.array([s[0], s[1],s[2]])
        dump_list.append([i+1,obbc,obbe,obbr,dirstring])
        #print(obbc)
        #link6.scale(s[0], s[1],s[2])
        #link6.translate([s[0]*-0.5, -0.5*s[1] ,-0.5*s[2]])
        #link6.transform(R,T)
        #shelf = world.makeTerrain(namelist[0])
        #shelf.geometry().set(link6)
        #shelf.appearance().setColor(0.2,0.6,0.3,1.0)
        #ff=open("obb_info/obb_info_"+sys.argv[1]+".pkl","wb")
    #print(voxel_list)
    #print(dump_list)
    #vis.debug(world)
    #pickle.dump(dump_list,ff)
    return dump_list

foldername=sys.argv[2]
filenumber=sys.argv[3]
world = klampt.WorldModel()
world.readFile(foldername+"/obstacles_"+filenumber+".xml")
print(foldername+"/obstacles_"+filenumber+".xml")
world1 = klampt.WorldModel()
world1.readFile("jaco_collision.xml")

collider_w = collide.WorldCollider(world)
num_ob = collider_w.world.numTerrains()

robot = world.robot(0)
robot1 = world1.robot(0)
qbase=robot.getConfig()
klampt.plan.motionplanning.setRandomSeed(2)

space = robotplanning.makeSpace(world1,robot1,edgeCheckResolution=0.005)
numqueries=int(sys.argv[1])
qarr=np.zeros((7*numqueries,3))
dirarr=[]
yarr=np.zeros((7*numqueries,1))
qarr_pose=np.zeros((numqueries,7))
yarr_pose=np.zeros((numqueries,1))
q= space.sample()
robot.setConfig(q)


colliderlist=[]
for lid in range(0,7):
    ignore=[]
    for igid in range(0,7):
            if igid==lid:
                continue
            ignore.append(robot.link(igid))
    collider=klampt.model.collide.WorldCollider(world,ignore=ignore)
    colliderlist.append(collider)
counter=0
coll_count=0
while counter<numqueries:
    feasible=0
    while feasible==0:
        q= space.sample()
        if space.isFeasible(q):
            feasible=1
            robot.setConfig(q)
            obbs=get_obbs(world,q)
            
            for lid in range(0,7):
                collider=colliderlist[lid]
                ans=1
                for it in range(0,num_ob):
                    check1=any(True for _ in collider.robotTerrainCollisions(robot.index,it))
                    if check1:
                        #print(q)
                        ans=0
                        #print("colliding")
                        break
                #yarr[counter]=ans
                #print(ans,obbs[lid][1])
                qarr[counter*7+lid]=obbs[lid][1]
                yarr[counter*7+lid]=ans
                dirarr.append(obbs[lid][4])
            ans=1
            for it in range(0,num_ob):
                check1=any(True for _ in collider_w.robotTerrainCollisions(robot.index,it))
                if check1:
                    #print("colliding")
                    coll_count+=1
                    ans=0
                    break
            q[2]+=3.97935067
            q[3]+=4.41568301
            qarr_pose[counter]=q #np.sin(q)
            yarr_pose[counter]=ans
            counter+=1
            #print(counter)

#print(dirarr)
#print(qarr)
print("collision count",coll_count, "out of ", numqueries)
f=open(foldername+"/obstacles_"+filenumber+"_coord.pkl","wb")
pickle.dump((qarr,dirarr,yarr),f)
f.close()
f=open(foldername+"/obstacles_"+filenumber+"_pose.pkl","wb")
pickle.dump((qarr_pose,yarr_pose),f)
f.close()
##robot.setConfig(qbase)



#vis.debug(world)
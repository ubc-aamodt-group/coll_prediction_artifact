import numpy as np
import sys
import random
import os.path
from os import path
import tqdm
import pickle

random.seed(1)

length = 0.07
xstart= -1.12
xend = 1.12
ystart = -1.12
yend=1.12
zstart=-1.12
zend=1.12

xlist=[]
t=xstart
while t<xend:
    xlist.append(t)
    t=t+length
#print(xlist)
ylist=[]
t=ystart
while t<yend:
    ylist.append(t)
    t=t+length

zlist=[]
t=zstart
while t<zend:
    zlist.append(t)
    t=t+length
#num_ob=sys.argv[1]

def find_nearest(x1,x2,xlist):
    for i in range(0,len(xlist)):
        if x1<xlist[i]:
            break
    lower= i-1
    for i in range(0,len(xlist)):
        if x2<=xlist[i]:
            break
    upper = i-1
    return(lower, upper)

def find_collision(x1,y1,z1,x2,y2,z2):
    list_voxels= []
    #print(x1,y1,z1,x2,y2,z2)
    x1,x2 = find_nearest(x1,x2,xlist)
    y1,y2 = find_nearest(y1,y2,ylist)
    z1,z2 = find_nearest(z1,z2,zlist)
    #print(x1,y1,z1,x2,y2,z2)
    for i in range(z1,z2+1):
        for j in range(y1,y2+1):
            for k in range(x1,x2+1):
                list_voxels.append((k,j,i))
    return list_voxels
def remove_dup(list_voxels):
    new =[]
    for i in list_voxels:
        if i not in new:
            new.append(i)
    return new
voxel_dict={}
color=["0.2 0.2 0.0","0.5 0.5 0.0","0.8 0.8 0.0"]
for num_ob in [3,6,9,12]:
    for i1 in range(0,len(zlist)):
                for j in range(0,len(ylist)):
                    for k in range(0,len(xlist)):
                        voxel_dict[(k,j,i1)]=0
    os.makedirs("scene_benchmarks/dens"+str(num_ob), exist_ok=True)
    #os.makedirs("voxel_object_collision/jaco/dens"+str(num_ob), exist_ok=True)
    #fvoxel=open("voxel_object_collision/jaco/dens"+str(num_ob)+"/summary.txt","w")
    print(num_ob)
    sum_voxels=0
    for i in tqdm.tqdm(range(0,100)):
        #num_ob = int(sys.argv[1])  # int(random.uniform(4,4))
        list_voxels=[]
        #fv= open("voxel_object_collision/jaco/dens"+str(num_ob)+"/scene_"+str(i)+".txt","w")

        f= open("scene_benchmarks/dens"+str(num_ob)+"/obstacles_"+str(i)+".xml","w")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<world>\n\t<robot name="jaco" file="../data/robots/jaco_mod.rob" translation="0.0 0.0 0" scale="1 1 1"/>\n')

        #print(num_ob)
        objects = int(random.uniform(num_ob,num_ob+2))
        for j in range(0,objects):
            #xscale=random.uniform(0.02,1.0)
            xscale=random.uniform(length*0,length*8)
            xpos=random.uniform(xstart,xend)
            yscale=random.uniform(length*0,length*8)
            ypos=random.uniform(ystart,yend)
            zscale=random.uniform(length*0,length*8)
            zpos=random.uniform(zstart,zend)
            f.write('\t\t<terrain file="../data/terrains/cube.off" scale="%f %f %f" translation="%f %f %f">\n'%(xscale,yscale,zscale,xpos,ypos,zpos))
            f.write('\t\t\t<display color="%s" opacity="0.2"/>\n'%(color[(j)%3]))
            f.write('\t\t</terrain>\n')

            temp=find_collision(xpos,ypos,zpos,xpos+xscale,ypos+yscale,zpos+zscale)
            list_voxels= list_voxels+ temp

        uniq_voxels= remove_dup(list_voxels)
        sum_voxels+=(len(uniq_voxels))

        for v in uniq_voxels:
            voxel_dict[v]+=1
            #fv.write("%s\n"%(str(v)))

        f.write("</world>")
        f.close()
        #fv.close()
    
import pickle
import numpy as np
import sys
#f=open("logfiles_GNN_link/link_info_"+str(sys.argv[1])+".pkl","rb")
f=open("logfiles_BIT_2D/link_info_"+str(sys.argv[1])+".pkl","rb")
(link_info,link_feas_info)=pickle.load(f)
f.close()
llx=[]
lly=[]
llz=[]

count=0
for edge in link_info:
    for pose in edge:
            count+=1
yarr=np.zeros((count,1))
qarr=np.zeros((count,2))
ymotionarr=[]
qmotionarr=[]
qmotionposearr=[] # for csp
ymotionposearr=[]
counter=0
for edge in link_info:
    qmotionarr.append([])
    qmotionposearr.append([])
    #print(edge)
    for pose in edge:
        #print(pose)
        qmotionposearr[-1].append([[pose[0],pose[1]]]) 
        qarr[counter]=[pose[0],pose[1]]
        counter+=1
        llx.append(pose[0])
        lly.append(pose[1])
    #print(len(i),i)
counter=0
colliding=0
for edge in link_feas_info:
    ymotionarr.append([])
    ymotionposearr.append([])
    for pose in edge:
        ymotionposearr[-1].append([pose])
        yarr[counter]=pose
        colliding+=pose
        counter+=1
print(counter,colliding)
#f=open("obstacles_gnn.pkl","wb")
#pickle.dump((qarr,[],yarr),f)
#f.close()
#f=open("obstacles_gnn_motiom.pkl","wb")
#pickle.dump((qmotionarr,[],ymotionarr),f)
#f.close()
f=open("logfiles_BIT_2D/coord_motiom_"+str(sys.argv[1])+".pkl","wb")
pickle.dump((qmotionposearr,ymotionposearr),f)
f.close()
#for edge in qmotionposearr:
#    print(edge)
f=open("logfiles_BIT_2D/coord_motiom_"+str(sys.argv[1])+".pkl","rb")
(qmotionposearr,ymotionposearr)=pickle.load(f)
f.close()
#print(ymotionposearr)
print(np.min(llx),np.max(llx))
print(np.min(lly),np.max(lly))
#print(np.min(llz),np.max(llz))

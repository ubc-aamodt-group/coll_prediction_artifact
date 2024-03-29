import pickle
import numpy as np
import sys
#f=open("logfiles_GNN_link/link_info_"+str(sys.argv[1])+".pkl","rb")
f=open("logfiles_BIT_link/link_info_"+str(sys.argv[1])+".pkl","rb")
(link_info,link_feas_info)=pickle.load(f)
f.close()
llx=[]
lly=[]
llz=[]

count=0
for edge in link_info:
    for pose in edge:
        for link in pose:
            count+=1
yarr=np.zeros((count,1))
qarr=np.zeros((count,3))
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
        qmotionposearr[-1].append([]) 
        for link in pose:  
            #print(link)
            qmotionposearr[-1][-1].append([link[0],link[1],link[2]])
            qmotionarr[-1].append([link[0],link[1],link[2]])   
            
            qarr[counter]=[link[0],link[1],link[2]]
            counter+=1
            llx.append(link[0])
            lly.append(link[1])
            llz.append(link[1])
    #print(len(i),i)
counter=0
colliding=0
for edge in link_feas_info:
    #print(edge)
    ymotionarr.append([])
    ymotionposearr.append([])
    for pose in edge:
        ymotionposearr[-1].append([])
        for link in pose:
            ymotionposearr[-1][-1].append(link)
            ymotionarr[-1].append(link)  
            yarr[counter]=link
            colliding+=link
            counter+=1
print(counter,colliding)
print(ymotionposearr)
#f=open("obstacles_gnn.pkl","wb")
#pickle.dump((qarr,[],yarr),f)
#f.close()
#f=open("obstacles_gnn_motiom.pkl","wb")
#pickle.dump((qmotionarr,[],ymotionarr),f)
#f.close()
f=open("logfiles_BIT_link/coord_motiom_"+str(sys.argv[1])+".pkl","wb")
pickle.dump((qmotionposearr,ymotionposearr),f)
f.close()
f=open("logfiles_BIT_link/coord_motiom_"+str(sys.argv[1])+".pkl","rb")
(qmotionposearr,ymotionposearr)=pickle.load(f)
f.close()
#print(ymotionposearr)
#print(np.min(llx),np.max(llx))
#print(np.min(lly),np.max(lly))
#print(np.min(llz),np.max(llz))

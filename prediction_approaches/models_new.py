import torch
import torch.nn as nn
from torch.autograd import Variable
import math
import torch.nn.functional as F

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed

class ResNet_nontied(nn.Module):
    # ResNet for regression of 3 Euler angles.
    def __init__(self, num_classes=256,num_bits=32):
        super(ResNet, self).__init__()
        #torch.normal(2, 3, size=(1, 4))
        self.code = torch.nn.Parameter(torch.normal(0,1,size=(num_bits,num_classes), dtype=torch.float, requires_grad=True).cuda())
        self.codeT = torch.nn.Parameter(torch.normal(0,1,size=(num_classes,num_bits), dtype=torch.float, requires_grad=True).cuda())
        self.tanh = nn.Tanh()


    def forward(self, x):
        x = torch.matmul(self.code,x)
        h = self.tanh(x)
        #print(self.code,x,h)
        #s = torch.matmul(torch.transpose(self.code,0,1),h)
        s = torch.matmul(self.codeT,x)
        
        return h,s #torch.cat((y,p,r),dim=1)

class ResNet(nn.Module):
    # ResNet for regression of 3 Euler angles.
    def __init__(self, num_classes=7,num_bits=2):
        super(ResNet, self).__init__()
        #torch.normal(2, 3, size=(1, 4))
        self.code = torch.nn.Parameter(torch.normal(0,1,size=(num_classes,num_bits), dtype=torch.float, requires_grad=True).cuda())
        self.tanh = nn.Tanh()


    def forward(self, x):
        #print(x,self.code)
        x = torch.matmul(x,self.code)
        #h = self.tanh(x)
        h=x
        #print(self.code,x,h)
        s = torch.matmul(h,torch.transpose(self.code,0,1))
        
        return h,s #torch.cat((y,p,r),dim=1)



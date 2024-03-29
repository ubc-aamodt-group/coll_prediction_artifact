
import matplotlib.pylab as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
import pandas as pd
import matplotlib
from sklearn.clusters import KMeans

file1 = open('logfile', 'r')
Lines = file1.readlines()
 
dataset = pd.read_csv('logfile_kuka2')
 
# distributing the dataset into two components X and Y
x = dataset.iloc[:, 0:7].values
y = dataset.iloc[:, 7].values

for i in range(10,11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X)

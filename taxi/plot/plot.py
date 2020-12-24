import pandas as pd
import os
import matplotlib.pyplot as plt

import numpy as np
from numpy.random import randn
import matplotlib as mpl
from scipy import stats

os.chdir("C:/Taxi_070220")

'''
file = pd.read_csv("duration.csv")

data1 = np.array(file['airport_duration'].tolist())
data2 = np.array(file['common_duration'].tolist())

#maxdata = np.r[data1, data2].max()
#bins = np.linspace(0, maxdata, maxdata+1)
bins = 10
labels = 'in town', 'from the airport'
plt.hist(data1, bins, normed=True, color="#ffce7b", alpha=.9,label=labels[1])
plt.hist(data2, bins, normed=True, color="#f3715c", alpha=.5,label=labels[0])
plt.xlabel("trip duration (s)")
plt.legend(loc='best')
'''

'''
file = pd.read_csv("distance.csv")

data1 = np.array(file['airport_distance'].tolist())
data2 = np.array(file['common_distance'].tolist())

bins = 10
labels = 'in town', 'from the airport'
plt.hist(data1, bins, normed=True, color="#ffce7b", alpha=.9,label=labels[1])
plt.hist(data2, bins, normed=True, color="#f3715c", alpha=.5,label=labels[0])
plt.xlabel("trip distance (km)")
plt.legend(loc='best')
'''


file = pd.read_csv("time_arrival.csv")

x = np.array(file['time of the day'].tolist())
data1 = np.array(file['arrival of cars'].tolist())
data2 = np.array(file['arrival of flights'].tolist())

labels = 'arrival of flights', 'arrival of cars'
plt.plot(x, data1, marker='o',ms=1,label=labels[1])
plt.plot(x, data2, marker='o',ms=1,label=labels[0])
plt.xlabel("time of the day")
plt.legend(loc='best')


'''
file = pd.read_csv("see.csv")

bins = 10
x = np.array(file['time'].tolist())
plt.hist(x, color="#90d7ec", alpha=.9)
plt.xlabel("waiting time (s)")
plt.ylabel("number")
'''



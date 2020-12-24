import os
import pandas as pd
import numpy as np

os.chdir("C:/Taxi_070220")

'''
a = 0.5465517027089453
d = pd.read_csv("d.csv")
s = pd.read_csv("s.csv")
f = pd.read_csv("f.csv")
#f_plus_1 = pd.read_csv("f_plus_1.csv")

to_process = pd.merge(s,f,how='left',on='car_id')
to_process = pd.merge(to_process,d,how='left',on='car_id')

#to_process = pd.merge(s,f_plus_1,how='left',on='car_id')
#to_process = pd.merge(to_process,d,how='left',on='car_id')

def cal_gain(r,c):
    # timesum - a * duration
    return r - a * c
    
to_process.loc[:,'gain'] = cal_gain(to_process['timesum'].values,to_process['duration'].values)

to_test = to_process[['gain','flights']]

to_test['is_gain'] = (to_test['gain'] > 0).astype('int')

to_test.corr()
'''

cars = pd.read_csv("hour_cars.csv")
flights = pd.read_csv("hour_flights.csv")
res = pd.merge(cars,flights,on='time')[['time','cars','flights']]

'''
import matplotlib.pyplot as plt
x = np.array(res['time'].tolist())
data1 = np.array(res['cars'].tolist())
data2 = np.array(res['flights'].tolist())
labels = 'arrival of flights', 'arrival of cars'
plt.plot(x, data1, marker='o',ms=1,label=labels[1])
plt.plot(x, data2, marker='o',ms=1,label=labels[0])
plt.xlabel("time of the day")
plt.legend(loc='best')
'''

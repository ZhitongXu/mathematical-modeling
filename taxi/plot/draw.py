import os
import pandas as pd

os.chdir("C:/Taxi_070220")

train = pd.read_csv('preparation.csv')

train['dropoff_time'] = pd.to_datetime(train.dropoff_time)
new = train.groupby(['car_id','dropoff_hour']).apply(lambda dropoff_time:(dropoff_time.max()-dropoff_time.min()))


new['waiting_time'] = 0
for i in range(len(new)):
    new['waiting_time'][i] = new['dropoff_time'][i].seconds
    
time = new[['waiting_time']]
time = time.reset_index()

time.groupby('dropoff_hour')['car_id'].count()

X = []
for i in range(24):
    X.append(i)
y = [9,5,4,3,3,6,3,8,8,9,12,8,13,14,12,14,13,19,17,12,12,14,10,13]
import matplotlib.pyplot as plt
plt.plot(X,y)
plt.xlabel("time of the day")
plt.ylabel("arrival of cars")


'''
to_draw = time[time['dropoff_hour'] > 9]
to_draw = to_draw[to_draw['dropoff_hour'] < 23]

X = []
for i in range(len(to_draw)):
    X.append(i)
    
import matplotlib.pyplot as plt
plt.hist(to_draw['waiting_time']/60)
plt.xlabel("waiting time(s)")
plt.ylabel("number")
'''



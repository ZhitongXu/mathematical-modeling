import os
import pandas as pd
import numpy as np
from math import sqrt
import datetime

os.chdir("C:/Taxi_070220")


duration = []
for p in range(1,101):
    train = pd.read_csv('Taxi (%d)' % p,header=None,names=['car_id','time','longitude','latitude','speed','angle','flag'])
    car_id = train['car_id'][0]
    def haversine_array(lat1, lng1, lat2, lng2):
        lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
        AVG_EARTH_RADIUS = 6371  # in km
        lat = lat2 - lat1
        lng = lng2 - lng1
        d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
        h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
        return h
    
    def geo_distance(lat1, lng1, lat2, lng2):
        a = haversine_array(lat1, lng1, lat1, lng2)
        b = haversine_array(lat1, lng1, lat2, lng1)
        return a + b
    
    def bridge_trip(x):
        return x['distance_to_bridge'] < 5
    
    train['bridge_lat'] = 31.19590
    train['bridge_lon'] = 121.34113
    
    train.loc[:, 'distance_to_bridge'] =  geo_distance(train['latitude'].values, train['longitude'].values, train['bridge_lat'].values, train['bridge_lon'].values)
    train['is_bridge'] = train.apply(bridge_trip,axis=1)
    test = train[train['is_bridge']]
    
    if not test.empty:
        r1 =  pd.DataFrame(columns=train.columns)
        r2 =  pd.DataFrame(columns=train.columns)
        for i in range(1,len(train)-1):
            if train['is_bridge'][i] == True and train['is_bridge'][i-1] == False:
                r1 = r1.append(train[i:i+1])
            if train['is_bridge'][i] == True and train['is_bridge'][i+1] == False:
                r2 = r2.append(train[i:i+1])
        r1['timescale'] = 0
        
        for j in range(len(r1)-1):
            t1 = datetime.datetime.strptime(r1['time'].values[j], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.datetime.strptime(r2['time'].values[j], "%Y-%m-%d %H:%M:%S")
            total_interval_time = (t2 - t1).total_seconds() 
            r1['timescale'].values[j] = total_interval_time
            
        duration.append([car_id,r1['timescale'].sum()])
        
d = np.matrix(duration)
d = pd.DataFrame(d)
d.to_csv("d.csv",index=False)
    

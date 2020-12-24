import os
import pandas as pd
import numpy as np

os.chdir("C:/Taxi_070220")

res = pd.DataFrame(columns=['car_id_x','dropoff_hour'])

for p in range(1,101):
    train = pd.read_csv('Taxi (%d)' % p,header=None,names=['car_id','time','longitude','latitude','speed','angle','flag'])
    
    car_id = train['car_id'][0]
    #train = pd.read_csv('Taxi (1)',header=None,names=['car_id','time','longitude','latitude','speed','angle','flag'])
    recordpick = pd.DataFrame(columns=['car_id','time','longitude','latitude','speed','angle','flag'])
    recorddrop = pd.DataFrame(columns=['car_id','time','longitude','latitude','speed','angle','flag'])
    for i in range(len(train)):
        if i == 0:
            recordpick = recordpick.append(train[i:i+1])
    
        if train.iloc[i,6]!=recordpick.iloc[len(recordpick)-1,6]:
            recordpick = recordpick.append(train[i:i+1])
            recorddrop = recorddrop.append(train[i-1:i])
        else:
            if recordpick.iloc[len(recordpick)-1,4] != 0 :
                if train.iloc[i,4] == 0 :
                    recordpick = recordpick.append(train[i:i+1])
                    recorddrop = recorddrop.append(train[i-1:i])
            if recordpick.iloc[len(recordpick)-1,4] == 0 :
                if train.iloc[i,4] != 0 :
                    recordpick = recordpick.append(train[i:i+1])
                    recorddrop = recorddrop.append(train[i-1:i])
    if len(recordpick) > len(recorddrop):
        recorddrop = recorddrop.append(train[len(train)-1:len(train)])
    
    recordpick['trip_id'] = range(len(recordpick))
    recorddrop['trip_id'] = range(len(recordpick))
    
    
    train = pd.merge(recordpick,recorddrop,on='trip_id')
    
    
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
        return x['dropoff_distance_to_bridge'] < 5
    
    train['bridge_lat'] = 31.19590
    train['bridge_lon'] = 121.34113
    
    train.loc[:, 'dropoff_distance_to_bridge'] =  geo_distance(train['latitude_y'].values, train['longitude_y'].values, train['bridge_lat'].values, train['bridge_lon'].values)
    train['dropoff_hour'] = pd.to_datetime(train.time_y).dt.hour + pd.to_datetime(train.time_y).dt.minute//30
    
    train['is_bridge'] = train.apply(bridge_trip,axis=1)
    train = train[train['is_bridge']]
    
    if not train.empty:
        subdf = train.drop_duplicates(['car_id_x','dropoff_hour'])
        
        subdf = subdf[['car_id_x','dropoff_hour']]
    
        res = res.append(subdf)
      
see = res.groupby('dropoff_hour')['car_id_x'].count()

see.to_csv("cars.csv",index=False)

    

    
    
    

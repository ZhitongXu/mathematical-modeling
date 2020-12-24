import os
import pandas as pd
import numpy as np

os.chdir("C:/Taxi_070220")

hour_flights_map = {
    0:32,
    1:15,
    2:1,
    3:2,
    4:9,
    5:17,
    6:9,
    7:17,
    8:20,
    9:49,
    10:66,
    11:47,
    12:44,
    13:55,
    14:59,
    15:68,
    16:64,
    17:59,
    18:58,
    19:55,
    20:61,
    21:52,
    22:62,
    23:66,
    24:32
}

added_flights = []

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
        
        a = subdf['dropoff_hour'].values.tolist()
        j = 0
        for i in subdf.index:
            subdf.loc[i,'num_of_flights'] = hour_flights_map[a[j]]
            j += 1
        
        res = subdf['num_of_flights'].sum()
    
        added_flights.append([car_id,res])
      
a = np.matrix(added_flights)
a = pd.DataFrame(a)
a.to_csv("f.csv",index=False)
    

    
    
    

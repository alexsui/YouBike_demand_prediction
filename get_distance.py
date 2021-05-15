from geopy import distance
import requests
url="https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json"
r=requests.get(url)
json_data=r.json()
bike_stop=json_data['retVal']
stop_number=['0001','0002','0003','0004','0005','0007','0011','0019','0025','0070','0075','0088','0113','0126','0138','0150','0187','0218','0282','0326']
Youbike_in_range={}
dis_800=[]
dis_600=[]
dis_1000=[]
dis_1200=[]
dis_1400=[]
farest_stop={}
#以市政府站為中心，依不同半徑抓取場站
target_stop_1=bike_stop['0001']
target_stop_1_pos=(target_stop_1['lat'],target_stop_1['lng'])
for i,stop in enumerate(stop_number):
    stop_pos=(bike_stop[stop]['lat'],bike_stop[stop]['lng'])
    dist=distance.distance(stop_pos,target_stop_1_pos).km
    if i==0:
        farest_stop={stop:dist}
    else:
        if list(farest_stop.values())[0]<dist:
            farest_stop={stop:dist}

    if dist < 0.6:
        dis_600.append(stop)
    if dist < 0.8:
        dis_800.append(stop)
    if dist < 1:
        dis_1000.append(stop)
    if dist < 1.2:
        dis_1200.append(stop)
    if dist < 1.4:
        dis_1400.append(stop)        
print(dis_600)
print(f"600m內數量{len(dis_600)}")
print(dis_800)
print(f"800m內數量{len(dis_800)}")
print(dis_1000)
print(f"1000m內數量{len(dis_1000)}")
print(dis_1200)
print(f"1200m內數量{len(dis_1200)}")
print(dis_1400)
print(f"1400m內數量{len(dis_1400)}")
print((f"最遠場站:{farest_stop}"))
print("-------------------------------------------")

#以西門站為中心抓取半徑2km場站
target_stop_2=bike_stop['0134']
target_stop_2_pos=(target_stop_2['lat'],target_stop_2['lng'])
in_range_of_0134=[]
dist_count=[]
list_of_bike_stop=list(bike_stop.keys())
for stop in list_of_bike_stop :
    stop_pos=(bike_stop[stop]['lat'],bike_stop[stop]['lng'])
    dist=distance.distance(stop_pos,target_stop_2_pos).km
    if dist<=2: #直接調動這邊的數字來過濾距離就好
        in_range_of_0134.append(stop)
        dist_count.append(dist)
print(dist_count)
print(f"芝山附近場站為:{in_range_of_0134}")
print(f"場站數量:{len(in_range_of_0134)}")
print("--------------------------------------------")
#以公館站為中心抓取半徑2km場站
target_stop_3=bike_stop['0045']
target_stop_3_pos=(target_stop_3['lat'],target_stop_3['lng'])
in_range_of_0045=[]
list_of_bike_stop=list(bike_stop.keys())
for stop in list_of_bike_stop :
    stop_pos=(bike_stop[stop]['lat'],bike_stop[stop]['lng'])
    dist=distance.distance(stop_pos,target_stop_3_pos).km
    if dist<=2:  #直接調動這邊的數字來過濾距離就好
        in_range_of_0045.append(stop)
print(f"公館場站為:{in_range_of_0045}")
print(f"場站數量:{len(in_range_of_0045)}")
import requests
import schedule
import time
import sqlite3
import schedule
con=sqlite3.connect('bike_count.db')
cur=con.cursor()


url="https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json"
r=requests.get(url)
json_data=r.json()
bike_stop=json_data['retVal']
stop_number=['0119','0184','0190','0210','0212','0216','0329']
bike_ratio=[]
bike_count=[]
for stop in stop_number:
    count=bike_stop[stop]['sbi']
    ratio=round(int(bike_stop[stop]['sbi'])/int(bike_stop[stop]['tot']),2)
    time=bike_stop[stop]['mday']
    bike_count.append(count)
    bike_ratio.append(ratio)
bike_ratio.insert(0,time)   
bike_count.insert(0,time)
Q1='''INSERT INTO Bike_count(time,stop_0119_count,stop_0184_count,stop_0190_count,stop_0210_count,stop_0212_count,stop_0216_count,stop_0329_count)VALUES(?,?,?,?,?,?,?,?)'''
Q2='''INSERT INTO Bike_ratio(time,stop_0119_ratio,stop_0184_ratio,stop_0190_ratio,stop_0210_ratio,stop_0212_ratio,stop_0216_ratio,stop_0329_ratio)VALUES(?,?,?,?,?,?,?,?)'''
cur.execute(Q1,tuple(bike_count))
cur.execute(Q2,tuple(bike_ratio))
con.commit()
con.close()
# schedule.every(5).minutes.do(get_YouBike_data)
# while True:
#     schedule.run_pending()
    









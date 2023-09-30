import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime,timezone,timedelta
import mysql.connector
from selenium.webdriver.chrome.options import Options
dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
dt2 = dt1.astimezone(timezone(timedelta(hours=8)))

def get_weather():
    url = "https://www.cwb.gov.tw/V8/C/W/OBS_Station.html?ID=46692"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver',
                            options=chrome_options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    temp = soup.find('td').find('span').get_text()
    wind = soup.find('td',{'headers':'w-2'}).find('span',{'class':'wind_1 is-active'}).get_text()
    humid = soup.find('td',{'headers':'hum'}).get_text()
    driver.close()
    return [temp,wind,humid]
def get_YouBike_data(list_of_stop,table,temp,wind,humid):
    db=mysql.connector.connect(
        host='34.80.95.3',
        user='user',
        passwd='root',
        database='Youbike'
        )
    cur=db.cursor()
    url="https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json"
    r=requests.get(url)
    json_data=r.json()
    bike_stop=json_data['retVal']
    stop_number=list_of_stop
    Youbike_data=[]
    for stop in stop_number:
        target_stop=bike_stop[stop]
        stop_name=target_stop['sno']
        tot=target_stop['tot']
        sbi=target_stop['sbi']
        lat=target_stop['lat']
        lng=target_stop['lng']
        time=dt2.strftime("%Y-%m-%d %H:%M:%S")
        data = (time,stop_name,tot,sbi,lat,lng,temp,wind,humid)
        Youbike_data.append(data)
    Q1='''INSERT INTO {}(time,stop,tot,sbi,lat,lng,temp,wind,humid)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''.format(table)
    cur.executemany(Q1,Youbike_data)
    db.commit()
    db.close()
list_of_Zhishan_stop=['0114', '0116', '0123', '0124', '0133', '0134', '0135', '0136', '0146', '0147', '0148', '0149', '0154', '0167', '0204', '0213', '0232', '0253', '0256', '0270', '0273', '0280', '0284', '0341', '0342', '0346', '0361', '0368', '0375', '0398']
list_of_TaipeiCityHall_stop=['0001','0002','0003','0004','0005','0007','0011','0019','0025','0070','0075','0088','0113','0126','0138','0150','0187','0218','0282','0326']
list_of_Gongguan_stop=['0030', '0031', '0036', '0038', '0045', '0054', '0057', '0061', '0062', '0066', '0081', '0098', '0102', '0104', '0126', '0128', '0132', '0168', '0181', '0182', '0252', '0289', '0293', '0295', '0296', '0304', '0306', '0315', '0350', '0353', '0362', '0364', '0399', '0400', '0405']
temp,wind,humid=get_weather()
get_YouBike_data(list_of_Zhishan_stop,'zhishan',temp,wind,humid)
get_YouBike_data(list_of_Gongguan_stop,'gongguan',temp,wind,humid)
get_YouBike_data(list_of_TaipeiCityHall_stop,'taipeiCityHall',temp,wind,humid)


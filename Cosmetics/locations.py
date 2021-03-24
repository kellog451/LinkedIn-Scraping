import re
import pandas as pd
from selenium import webdriver
from time import sleep
from random import randint

# specifies the path to the chromedriver.exe


driver = webdriver.Chrome('/Users/imaki/Desktop/chromedriver')
# ('/Users/imaki/Desktop/chromedriver')

df = pd.read_csv('Extracted_csv/CosmeticsData.csv')
Location_Array = df['Location']
Names_Array = df['Company Name']

Coordinates = []
Latitudes = []
Longitudes = []

i = 0
while i < len(Location_Array):

    # search by location or company name:
    if not str(Location_Array[i]).strip():
        query = str(Names_Array[i])
    else:
        query = str(Location_Array[i])

    theurl = 'http://api.positionstack.com/v1/forward?access_key=5c9f88eb89d0d541f1ca70c80d11d868&query='+query+'&country=AU'

    # sleep(randint(5, 10))
    # driver.get method() will navigate to a page given by the URL address
    driver.get(theurl)

    data = driver.find_element_by_xpath("//pre").text

    x = re.search('latitude":(.+?),"longitude"', data)

    if x:
        lat = x.group(1)
    else:
        lat = ''

    y = re.search('longitude":(.+?),"type"', data)

    if y:
        long = y.group(1)
    else:
        long = ''

    if lat:
        latt = str(lat)
    else:
        latt = ' '

    if long:
        longg = str(long)
    else:
        longg = ' '

    Latitudes.append(latt)
    Longitudes.append(longg)
    print('Request: ' + str(i))
    i += 1

loc_data = pd.DataFrame({
    'Latitude': Latitudes,
    'Longitude': Longitudes
})

print(loc_data)

loc_data.to_csv("Extracted_csv/LocationData.csv", mode='a', index=False, header=False)

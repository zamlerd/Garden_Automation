#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from geopy.geocoders import Nominatim
import datetime 
import sys, requests
from datetime import timedelta

pd.options.display.max_rows = 4000

DARK_SKY_API_KEY = "Your_Key_Here"
option_list = "exclude=currently,minutely,hourly,alerts&amp;units=si"


now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
numList = [str(year), str(month), str(day)]
seperator = '-'

location = Nominatim().geocode("Houston", language='en_US')
d_from_date = datetime.datetime.strptime(seperator.join(numList) , '%Y-%m-%d')
d_to_date = datetime.datetime.strptime(seperator.join(numList) , '%Y-%m-%d')

delta = d_to_date - d_from_date
latitude = str(location.latitude)
longitude = str(location.longitude)


print("\nLocation: "+ location.address)
for i in range(delta.days+1):
  new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
  search_date = new_date+"T00:00:00"
  response = requests.get("https://api.darksky.net/forecast/"+DARK_SKY_API_KEY+"/"+latitude+","+longitude+","+search_date+"?"+option_list)
  json_res = response.json()
    
print("\n"+(d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A'))
unit_type = '°F' if json_res['flags']['units'] == 'us' else '°C'
print("Min temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMin'])+unit_type)
print("Max temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMax'])+unit_type)
print("Summary: " + json_res['daily']['data'][0]['summary'])
precip_type = None
precip_prob = None
if'precipProbability' in json_res['daily']['data'][0] and 'precipType' in json_res['daily']['data'][0]:
    precip_type = json_res['daily']['data'][0]['precipType']
    precip_prob = json_res['daily']['data'][0]['precipProbability']
if (precip_type == 'rain' and precip_prob != None):
    precip_prob *= 100
print("Chance of rain: %.2f%%" % (precip_prob))

out_df = pd.read_csv("/Users/dzamler/Documents/Personal/Ethnogardenv2.csv")
danger_df = out_df.loc[out_df["Temp_Min"] >= json_res['daily']['data'][0]['apparentTemperatureMin']]
if danger_df.empty == True:
    print("All Plants are Safe!")
else:
    move_df = danger_df.loc[danger_df["Inside"] != "1"]
    print("Move these to Safety!")
    print(move_df["Latin Name"])


# In[4]:


import os

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

# Calling the function
#notify(title    = 'Move these to Safety!',
#       message = i for i in move_df["Latin Name"],
#       subtitle  = 'Hello, this is me, notifying you!')


# In[ ]:





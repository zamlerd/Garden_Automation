#!/usr/bin/env python
# coding: utf-8

# In[50]:


# Python program to find current  
# weather details of any city 
# using openweathermap api 
  
# import required modules 
import requests, json, csv
import pandas as pd
  
# Enter your API key here 
api_key = "da2ef94ca1c7f76a4dee352a372cef81"
  
# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
# Give city name 
city_name = "Houston" 
  
# complete_url variable to store 
# complete url address 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
  
# get method of requests module 
# return response object 
response = requests.get(complete_url) 
  
# json method of response object  
# convert json format data into 
# python format data 
x = response.json() 
#print(x)
  
# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
if x["cod"] != "404": 
  
    # store the value of "main" 
    # key in variable y 
    y = x["main"] 
  
    # store the value corresponding 
    # to the "temp" key of y 
    current_temperature = y["temp_min"]
    
    current_temperature = (float(current_temperature) - 273.15) * (9/5) +32
  
    # store the value corresponding 
    # to the "pressure" key of y 
    current_pressure = y["pressure"] 
  
    # store the value corresponding 
    # to the "humidity" key of y 
    current_humidiy = y["humidity"] 
  
    # store the value of "weather" 
    # key in variable z 
    z = x["weather"] 
  
    # store the value corresponding  
    # to the "description" key at  
    # the 0th index of z 
    weather_description = z[0]["description"] 
  
    # print following values 
    #print(" Mininmum Temperature *F = " +
                    #str(current_temperature) + 
          #"\n atmospheric pressure (in hPa unit) = " +
                    #str(current_pressure) +
          #"\n humidity (in percentage) = " +
                    #str(current_humidiy) +
          #"\n description = " +
                    #str(weather_description)) 
  
else: 
    print(" City Not Found ") 

    
out_df = pd.read_csv("/Users/dzamler/Documents/Personal/Ethnogarden.csv")
move_df = out_df.loc[out_df["Temp_Min"] >= current_temperature]
if move_df.empty == True:
    print("All Plants are Safe!")
else:
    print("Move these to Safety!")
    print(move_df["Latin Name"])


# In[ ]:





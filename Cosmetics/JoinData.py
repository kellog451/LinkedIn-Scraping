import pandas as pd
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup

column_names = ["Latitude", "Longitude"]
df = pd.read_csv('Extracted_csv/LocationData.csv', names=column_names)
Lat_Array = df['Latitude'].to_list()
Long_Array = df['Longitude'].to_list()

df = pd.read_csv("Extracted_csv/CosmeticsData.csv")
df["Latitude"] = Lat_Array
df["Longitude"] = Long_Array
df.to_csv("Extracted_csv/CosmeticsData.csv", index=False)

# ourdata.to_csv("otherLinks.csv", index=False, header=False)

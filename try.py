# Code for PhD project on traffic management
# Iaroslav Kriuchkov
# Aalto University

import pandas as pd
import numpy as np

# Function for downloading csv data from an automatic traffic monitoring system of Finnish Transport Agency
# url is the link to the exact file
# function returns the Pandas DataFrame with the data from specific TMS point on specific year on specific day
def data_import (tms_id, region, year, day):
    column_names = ['id', 'year', 'day', 'hour', 'minute', 'second', '1/100 second', 'length', 'lane', 'direction', 'vehicle', 'speed', 'faulty', 'Total time', 'Time interval', 'Queue start' ]
    df = pd.DataFrame()
    url = 'https://aineistot.liikennevirasto.fi/lam/rawdata/YYYY/REGION_ID/lamraw_TMS_YY_DD.csv'
    url = url.replace('YYYY', str(year)).replace('REGION_ID', region).replace('TMS', tms_id).replace('YY', str(year)[2:4]).replace('DD', str(day))
    df = pd.read_csv(url, delimiter = ";", names = column_names)
    return df

df = pd.DataFrame() 
df = data_import('101', '01', 2017, 1)
print(df.head())
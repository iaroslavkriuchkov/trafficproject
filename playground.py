import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import requests

downdload_list = ['117', '01', 2017, 100]

def file_import (tms_id, region, year, day, delete_if_faulty = True, create_dates = True, split_directions = True):
    start_time = time.perf_counter() 
    column_names = ['id', 'year', 'day', 'hour', 'minute', 'second', 'hund_second', 'length', 'lane', 'direction', 'vehicle', 'speed', 'faulty', 'total_time', 'time_interval', 'queue_start']
    dfdir1 = pd.DataFrame()
    dfdir2 = pd.DataFrame()
    url = 'https://aineistot.liikennevirasto.fi/lam/rawdata/YYYY/REGION_ID/lamraw_TMS_YY_DD.csv'
    url = url.replace('YYYY', str(year)).replace('REGION_ID', region).replace('TMS', tms_id).replace('YY', str(year)[2:4]).replace('DD', str(day))
    if requests.get(url).status_code != 404:
        dfdir1 = pd.read_csv(url, delimiter = ";", names = column_names)
        print(f"Download successful - file for the sensor {tms_id} for the day {day} in year {year}")
        dfdir1 = dfdir1[dfdir1.faulty != 1]
        dfdir2 = dfdir1.groupby(dfdir1.direction).get_group(2).reset_index()
        #dfdir2 = dfdir2.drop('index', axis=1, inplace=True)
        dfdir1 = dfdir1[dfdir1.direction != 2].reset_index()
    else:
        print(f"File for the sensor {tms_id} for the day {day} in year {year} doesn't exist. ")
    end_time = time.perf_counter()
    print(f"Download took {end_time-start_time:0.4f} seconds")
    return dfdir1, dfdir2

df1 = pd.DataFrame()
df2 = pd.DataFrame()

df1, df2 = file_import(downdload_list[0], downdload_list[1], downdload_list[2], downdload_list[3])

print(df1.head())
print(df2.head())
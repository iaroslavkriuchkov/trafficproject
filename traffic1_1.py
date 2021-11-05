# Code for PhD project on traffic management
# Iaroslav Kriuchkov
# Aalto University School of Business
# Department of Information and Service Management
# Last update on 05 November 2021

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import requests

downdload_list = [['162', '01', 2017, 100],['162', '01', 2017, 101], ['162', '01', 2017, 102], ['162', '01', 2017, 103], ['162', '01', 2017, 104],['162', '01', 2017, 105]]

# Function for downloading csv_file from an automatic traffic monitoring system of Finnish Transport Agency
# url is the link to the exact file
# The function returns the Pandas DataFrame with the data from specific TMS point on specific year on specific day
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
        for i in range(len(dfdir1)):
            if dfdir1.at[i, "faulty"]== 1:
                dfdir1.drop(i, axis=0, inplace=True)
    else:
        print(f"File for the sensor {tms_id} for the day {day} in year {year} doesn't exist. ")
    end_time = time.perf_counter()
    print(f"Download took {end_time-start_time:0.4f} seconds")
    return dfdir1, dfdir2

# Function for downloading a massive of csv_files of TMS points
def data_import(input_list):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    for i in range(len(input_list)):
        if i == 0:
            df = file_import(input_list[i][0], input_list[i][1], input_list[i][2], input_list[i][3])
        else :
            df1 = file_import(input_list[i][0], input_list[i][1], input_list[i][2], input_list[i][3])
            df = df.append(df1, ignore_index=True)
    return df

# Calculation of flow and speed lists. Mode 0 is the arithmetic mean of speed, mode 1 is the harmonic mean of speed
def flow_speed_calculation (df, aggregation_time_period, mode):
    start_time = time.perf_counter() 
    flow_speed = pd.DataFrame()
    flow_speed['flow'] = [0 for i in range(int(24*60/aggregation_time_period))]
    flow_speed['total_speed'] = [0.0 for i in range(int(24*60/aggregation_time_period))]
    flow_speed['mean_speed'] = [0.0 for i in range(int(24*60/aggregation_time_period))]
#   '''
    if mode == 0:
        for i in range(len(df)):      
            flow_speed.at[int(df["total_time"][i]/(aggregation_time_period*60*100)), 'flow'] += 1
            flow_speed.at[int(df["total_time"][i]/(aggregation_time_period*60*100)), 'total_speed'] += df.at[i, 'speed']
        flow_speed['mean_speed'] = flow_speed['total_speed'].div(flow_speed['flow'].values)
    elif mode == 1:
        for i in range(len(df)):    
            flow_speed.at[int(df["total_time"][i]/(aggregation_time_period*60*100)), 'flow'] += 1
            flow_speed.at[int(df["total_time"][i]/(aggregation_time_period*60*100)), 'total_speed'] += (1 / df.at[i, "speed"])
        flow_speed['mean_speed'] = flow_speed['flow'].div(flow_speed['total_speed'].values)
    end_time = time.perf_counter()
    print(f"Execution time {end_time-start_time:0.4f} seconds")

    return flow_speed

# The DataFrame is created based on downloaded data
df = pd.DataFrame() 
df = data_import(downdload_list)
print(df.head())
print(len(df))

# aggregation_time_period shows the period, by which the data is aggregated (in minutes)  
aggregation_time_period = 1

flow_speed = flow_speed_calculation(df, aggregation_time_period, 1)
print(flow_speed.describe())

# The scatter plot in speed-flow plane
plt.scatter(flow_speed.flow, flow_speed.mean_speed)
plt.show()


# Code for PhD project on traffic management
# Iaroslav Kriuchkov
# Aalto University School of Business
# Department of Information and Service Management
# Last update on 05 November 2021

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pandas.core.algorithms import value_counts
import requests
import datetime

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
        dfdir1['date'] = datetime.date(year, 1, 1) + datetime.timedelta(day - 1)
        dfdir1 = dfdir1[dfdir1.faulty != 1]
        dfdir2 = dfdir1.groupby(dfdir1.direction).get_group(2).reset_index()
        dfdir1 = dfdir1[dfdir1.direction != 2].reset_index()
    else:
        print(f"File for the sensor {tms_id} for the day {day} in year {year} doesn't exist. ")
    end_time = time.perf_counter()
    print(f"Download took {end_time-start_time:0.4f} seconds")
    return dfdir1, dfdir2

# Function for downloading a massive of csv_files of TMS points
def data_import(input_list):
    df_list =[]
    for i in range(len(input_list)):
        df1, df2 = file_import(input_list[i][0], input_list[i][1], input_list[i][2], input_list[i][3])
        df_list.append(df1)
        df_list.append(df2)
        #[input_list[0],datetime.date(input_list[2], 1, 1) + datetime.timedelta(input_list[3] - 1), df1, df2])
    return df_list

# Calculation of flow and speed lists. Mode 0 is the arithmetic mean of speed, mode 1 is the harmonic mean of speed
def flow_speed_calculation (df_list, aggregation_time_period, mode):
    start_time = time.perf_counter()
    for i in range(len(df_list)):
        df_list[i]['Aggregation'] = (df_list[i].hour * 60 + df_list[i].minute)/aggregation_time_period
        df_list[i] = df_list[i].astype({'Aggregation':int})  
    print(df_list)
    flow_speed = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df1 = df_list[0].Aggregation.value_counts().sort_index()
    #df1.columns = ['aggregation', 'flow']
    df2 = df_list[0].speed.groupby(by=df_list[0].Aggregation).mean()
    #df2.columns = ['aggregation', 'speed']
    plt.scatter(df1, df2)
    '''
    flow_speed['flow'] = [0 for i in range(int(24*60/aggregation_time_period))]
    flow_speed['total_speed'] = [0.0 for i in range(int(24*60/aggregation_time_period))]
    flow_speed['mean_speed'] = [0.0 for i in range(int(24*60/aggregation_time_period))]
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
    '''
    end_time = time.perf_counter()
    print(f"Execution time {end_time-start_time:0.4f} seconds")
    print(df1)
    print(df2)
    return flow_speed

# The DataFrame is created based on downloaded data
df = pd.DataFrame() 
data_list = [[]]
data_list = data_import(downdload_list)
#print(data_list)
aggregation_time_period = 10
flow_speed_calculation(data_list, aggregation_time_period, 1)
#print(df.head())
#print(len(df))
'''
# aggregation_time_period shows the period, by which the data is aggregated (in minutes)  
aggregation_time_period = 1

flow_speed = flow_speed_calculation(df, aggregation_time_period, 1)
print(flow_speed.describe())

# The scatter plot in speed-flow plane
plt.scatter(flow_speed.flow, flow_speed.mean_speed)
plt.show()

'''
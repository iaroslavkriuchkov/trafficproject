# Code for PhD project on traffic management
# Iaroslav Kriuchkov
# Aalto University School of Business
# Department of Information and Service Management
# Last update on 09 November 2021

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pandas.core.algorithms import value_counts
import requests
import datetime
from scipy.stats.mstats import hmean
import os
import pathlib
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

def local_file_import (file_path, year, day, delete_if_faulty = True, create_dates = True, split_directions = True):
    start_time = time.perf_counter() 
    column_names = ['id', 'year', 'day', 'hour', 'minute', 'second', 'hund_second', 'length', 'lane', 'direction', 'vehicle', 'speed', 'faulty', 'total_time', 'time_interval', 'queue_start']
    dfdir1 = pd.DataFrame()
    dfdir2 = pd.DataFrame()
    if os.path.exists(file_path) == True:
        dfdir1 = pd.read_csv(file_path, delimiter = ";", names = column_names)
        print(f"Download successful - file {file_path}")
        dfdir1['date'] = datetime.date(year, 1, 1) + datetime.timedelta(day - 1)
        dfdir1 = dfdir1[dfdir1.faulty != 1]
        dfdir2 = dfdir1.groupby(dfdir1.direction).get_group(2).reset_index()
        dfdir1 = dfdir1[dfdir1.direction != 2].reset_index()
    else:
        print(f"File {file_path} doesn't exist. ")
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
    return df_list

def local_data_import(folder):
    df_list = []
    directory = pathlib.Path(folder)
    for day in range(303, 308):
        file_name = 'lamraw_'+folder.split('_')[2]+'_'+folder.split('_')[1]+'_'+str(day+1)+'.csv'
        location = directory / file_name
        df1, df2 = local_file_import(location, 2021, day)
        df_list.append(df1)
        df_list.append(df2)
        print(df_list)
    return df_list

# Calculation of flow and speed lists. Mode 0 is the arithmetic mean of speed, mode 1 is the harmonic mean of speed
def flow_speed_calculation (df_list, aggregation_time_period, mode):
    start_time = time.perf_counter()
    for i in range(len(df_list)):
        df_list[i]['aggregation'] = (df_list[i].hour * 60 + df_list[i].minute)/aggregation_time_period
        df_list[i] = df_list[i].astype({'aggregation':int})  
    print(df_list)
    flow_speed = pd.DataFrame()
    if mode == 0:
        for i in range(len(df_list)):
            if i == 0:
                flow_speed = df_list[i].groupby(['id','date', 'aggregation', 'direction'], as_index = False).agg(mean_speed=('speed','mean'), flow = ('speed','count'))
            else:
                flow_speed = flow_speed.append(df_list[i].groupby(['id','date', 'aggregation', 'direction'], as_index = False).agg(mean_speed=('speed','mean'), flow = ('speed','count')), ignore_index=True)
            print(flow_speed)
    elif mode == 1:
        for i in range(len(df_list)):
            if i == 0:
                flow_speed = df_list[i].groupby(['id','date', 'aggregation', 'direction'], as_index = False).agg(mean_speed=('speed',hmean), flow = ('speed','count'))
            else:
                flow_speed = flow_speed.append(df_list[i].groupby(['id','date', 'aggregation', 'direction'], as_index = False).agg(mean_speed=('speed',hmean), flow = ('speed','count')), ignore_index=True)
            print(flow_speed)
    flow_speed['density'] = flow_speed['flow'].div(flow_speed['mean_speed'].values)
    print(flow_speed)
    end_time = time.perf_counter()
    print(f"Execution time {end_time-start_time:0.4f} seconds")
    return flow_speed

# The DataFrame is created based on downloaded data
df = pd.DataFrame() 
import_list = []
for i in range(208):
    import_list.append(['116', '01', 2021, i+1])

for i in range(209, 298):
    import_list.append(['116', '01', 2021, i+1])

for i in range(300, 312):
    import_list.append(['116', '01', 2021, i+1])


aggregation_time_period = 5
data_list = data_import(import_list)

flow_speed = flow_speed_calculation(data_list, aggregation_time_period, 0)

plt.scatter(flow_speed.density, flow_speed.flow)
plt.show()
'''
path = 'trafficproject/data_21_116'
data_list = local_data_import(path)

aggregation_time_period = 2
df1 = flow_speed_calculation(data_list, aggregation_time_period, 1)
print(df1.mean_speed.describe)
plt.scatter(df1.density, df1.flow)
#plt.show()
#plt.scatter(df1.density, df1.flow)
#plt.hist(df1.mean_speed)
plt.show()

# aggregation_time_period shows the period, by which the data is aggregated (in minutes)  
aggregation_time_period = 1

flow_speed = flow_speed_calculation(df, aggregation_time_period, 1)
print(flow_speed.describe())

# The scatter plot in speed-flow plane
plt.scatter(flow_speed.flow, flow_speed.mean_speed)
plt.show()

'''
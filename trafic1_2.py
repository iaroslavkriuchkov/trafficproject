# Code for PhD project on traffic management
# Iaroslav Kriuchkov
# Aalto University School of Business
# Department of Information and Service Management
# Last update on 09 November 2021
# Calculation on id 126 for 1 week

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

# Function for downloading csv_file from an automatic traffic monitoring system of Finnish Transport Agency
# url is the link to the exact file
# The function returns the Pandas DataFrame with the data from specific TMS point on specific year on specific day
'''
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
'''
def local_file_import (file_path, year, day, delete_if_faulty = True, create_dates = True, split_directions = True):
    start_time = time.perf_counter() 
    column_names = ['id', 'year', 'day', 'hour', 'minute', 'second', 'hund_second', 'length', 'lane', 'direction', 'vehicle', 'speed', 'faulty', 'total_time', 'time_interval', 'queue_start']
    dfdir1 = pd.DataFrame()
    if os.path.exists(file_path) == True:
        dfdir1 = pd.read_csv(file_path, delimiter = ";", names = column_names)
        print(f"Download successful - file {file_path}")
        dfdir1['date'] = datetime.date(year, 1, 1) + datetime.timedelta(day - 1)
        dfdir1 = dfdir1[dfdir1.faulty != 1]
    else:
        print(f"File {file_path} doesn't exist. ")
    end_time = time.perf_counter()
    print(f"Download took {end_time-start_time:0.4f} seconds")
    return dfdir1
'''
# Function for downloading a massive of csv_files of TMS points
def data_import(input_list):
    df_list =[]
    for i in range(len(input_list)):
        df1, df2 = file_import(input_list[i][0], input_list[i][1], input_list[i][2], input_list[i][3])
        df_list.append(df1)
        df_list.append(df2)
    return df_list
'''
def local_data_import(folder):
    df = pd.DataFrame()
    directory = pathlib.Path(folder)
    for day in range(270, 360):
        file_name = 'lamraw_'+folder.split('_')[2]+'_'+folder.split('_')[1]+'_'+str(day+1)+'.csv'
        location = directory / file_name
        if (df.empty):
            df = local_file_import(location, 2018, day)
        else:
            df = df.append(local_file_import(location, 2018, day), ignore_index=True)
 #       print(df)
    return df

# Calculation of flow and speed lists. Mode 0 is the arithmetic mean of speed, mode 1 is the harmonic mean of speed
def flow_speed_calculation (df, aggregation_time_period):
    start_time = time.perf_counter()
    df['aggregation'] = (df.hour * 60 + df.minute)/aggregation_time_period
    df = df.astype({'aggregation':int})  
    print(df)
    time_agg = pd.DataFrame()
    space_agg = pd.DataFrame()
    time_agg = df.groupby(['id','date', 'aggregation', 'direction', 'lane'], as_index = False).agg(time_mean_speed=('speed','mean'), flow = ('speed','count'))
    time_agg['qdivv'] = time_agg['flow'].div(time_agg['time_mean_speed'].values)
    print(time_agg)
    space_agg = time_agg.groupby(['id','date', 'aggregation', 'direction'], as_index = False).agg(qdivvsum = ('qdivv', 'sum'), flow = ('flow', 'sum'))
    space_agg['space_mean_speed'] = 1/(space_agg.qdivvsum.div(space_agg.flow))
    space_agg['density'] = space_agg.flow.div(space_agg.space_mean_speed)
    print(space_agg)
    end_time = time.perf_counter()
    print(f"Execution time {end_time-start_time:0.4f} seconds")
    return space_agg

# The DataFrame is created based on downloaded data
df = pd.DataFrame() 

path = 'trafficproject/data_19_11'
df = local_data_import(path)
aggregation_time_period = 10
flow_speed = flow_speed_calculation(df, aggregation_time_period)
'''
aggregation_time_period = 1
data_list = local_data_import(path)

flow_speed = flow_speed_calculation(data_list, aggregation_time_period, 0)
'''
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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pandas.core.algorithms import value_counts
import requests
import datetime
from scipy.stats.mstats import hmean
import pathlib

url = 'https://aineistot.liikennevirasto.fi/lam/rawdata/2019/01/lamraw_11_19_DD.csv'
for day in range(365):
    url = url.replace('DD', str(day+1))
    start_time = time.perf_counter()  
    req = requests.get(url)
    if requests.get(url).status_code != 404:
        url_content = req.content
        filename = 'lamraw_11_19_DD.csv'
        csv_file = open(filename.replace('DD', str(day+1)), 'wb')
        csv_file.write(url_content)
        csv_file.close()
        end_time = time.perf_counter()
        print(f"Download of {filename.replace('DD', str(day+1))} took {end_time-start_time:0.4f} seconds")
    else:
        print(f"File doesn't exist.")
    url = 'https://aineistot.liikennevirasto.fi/lam/rawdata/2019/01/lamraw_11_19_DD.csv'

'''
current_dir = pathlib.Path.cwd()
print(current_dir)
for day in range(303, 308):
    path = 'trafficproject/data_21_116'
    data_folder = pathlib.Path(path)
    file_name = 'lamraw_'+path.split('_')[2]+'_'+path.split('_')[1]+'_'+str(day+1)+'.csv'
    location = data_folder / file_name
    print(location)
    column_names = ['id', 'year', 'day', 'hour', 'minute', 'second', 'hund_second', 'length', 'lane', 'direction', 'vehicle', 'speed', 'faulty', 'total_time', 'time_interval', 'queue_start']
    df=pd.read_csv(location, delimiter=';', names = column_names)
    print(df.head())

data_list = []
for i in range(308):
    data_list.append(['116', '01', 2021, i+1])

print(data_list)
'''
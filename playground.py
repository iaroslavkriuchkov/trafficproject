import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pandas.core.algorithms import value_counts
import requests
import datetime
from scipy.stats.mstats import hmean
import pathlib

url = 'https://aineistot.liikennevirasto.fi/lam/rawdata/2019/01/lamraw_10_19_DD.csv'
for day in range(365):
    start_time = time.perf_counter()  
    url = url.replace('DD', str(day+1))
    req = requests.get(url)
    if requests.get(url).status_code != 404:
        url_content = req.content
        filename = 'lamraw_10_19_DD.csv'
        csv_file = open(filename.replace('DD', str(day+1)), 'wb')
        csv_file.write(url_content)
        csv_file.close()
        end_time = time.perf_counter()
        print(f"Download of {filename.replace('DD', str(day+1))} took {end_time-start_time:0.4f} seconds")
    else:
        print(f"File doesn't exist.")

'''
current_dir = pathlib.Path.cwd()
print(current_dir)
for day in range(5):
    path = 'trafficproject/data_17_146'
    data_folder = pathlib.Path(path)
    file_name = 'lamraw_'+path.split('_')[2]+'_'+path.split('_')[1]+'_'+str(day+1)+'.csv'
    location = data_folder / file_name
    print(location)
    df=pd.read_csv(location, delimiter=';')
    print(df.head)
'''
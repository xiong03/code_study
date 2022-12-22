# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 21:04:12 2022

@author: xiong
"""

from import_me_data import get_station_by_xy,get_data_by_stations
import pandas as pd
import os

db='meteodata'
sql_name='root'
pwd='123456'
host='192.168.118.158'
port=3306

# data = get_data_by_xy([40,130],[20,60],['DMNT','DMXT'],'2000','2020',db,sql_name,pwd,host,port)
station = get_station_by_xy([40,130],[20,60],db,sql_name,pwd,host,port)
code_sta = station['code'].tolist()
data = get_data_by_stations(code_sta, ['DMNT','DMXT'], '2000-01-01', '2020-01-01', db,sql_name,pwd,host,port,True)
s_x_y = station[['code','X','Y']].copy()
s_x_y.columns = ['SID','LAT','LON']
s_x_y.set_index(['SID'],inplace=True)


for year in range(2000,2021):
    min_result,max_result = [pd.DataFrame(),pd.DataFrame()]
    df1 = data[data['DATE'].astype(str).str.contains(str(year))].copy()
    
    df1_min = df1[['Station','DATE','DMNT']].copy()
    df1_max = df1[['Station','DATE','DMXT']].copy()
    
    df1_min = df1_min.pivot(index=["Station"],columns=["DATE"],values=["DMNT"])
    df1_max = df1_max.pivot(index=["Station"],columns=["DATE"],values=["DMXT"])
    for i in range(int(df1_max.shape[1]/16)+1):
        min_temp = df1_min.iloc[:,i*16:(i+1)*16].mean(1).copy()
        max_temp = df1_max.iloc[:,i*16:(i+1)*16].mean(1).copy()
        
        min_result = pd.concat([min_result,min_temp],axis=1)
        max_result = pd.concat([max_result,max_temp],axis=1)
        
    min_result.columns = [i for i in range(int(df1_max.shape[1]/16)+1)]
    max_result.columns = [i for i in range(int(df1_max.shape[1]/16)+1)]
    
    result_min = pd.concat([s_x_y,min_result],axis=1,join ='inner')
    result_max = pd.concat([s_x_y,max_result],axis=1,join ='inner')
    
    result_min.reset_index(inplace=True)
    result_min.rename(columns={'index':'SID'},inplace=True)
    result_max.reset_index(inplace=True)
    result_max.rename(columns={'index':'SID'},inplace=True)
    
    out_min = r"C:\Users\xiong\Downloads\DMNT"+os.sep+'DMNT'+'_'+str(year)+'.txt'
    out_max = r"C:\Users\xiong\Downloads\DMXT"+os.sep+'DMXT'+'_'+str(year)+'.txt'
    
    result_min.to_csv(out_min,sep=',',index=False,header=True,float_format='%.2f')
    result_max.to_csv(out_max,sep=',',index=False,header=True,float_format='%.2f')
    print('successful ',year)
    
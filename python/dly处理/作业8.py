# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 08:53:55 2022

@author: xiong
"""

import pandas as pd
import glob
import os

path = r"D:\python作业\dly处理"
names = ['PRCP','SNOW','SNWD','TMAX']
dly_paths = glob.glob(path+os.sep+"*.dly")
df2 = pd.DataFrame()
for dly_path,dly in zip(dly_paths,["AM4","AM0"]):
    width=[11,4,2,4]
    for i in range(31):
        width.append(5)
        width.append(3)
    dly_df = pd.read_fwf(dly_path,widths=width,header = None)
    dly_df.replace(-9999,'nan',inplace = True)
    df = dly_df.iloc[:,0:4]
    df.set_axis(['姓名','年份','月份','类型'], axis='columns', inplace=True)
    for i in range(1,32):
        df[i] = dly_df.iloc[:,2*i+2:2*i+3]
    df.set_index('类型',inplace=True)
    for name in names:
        if name in df.index:
            df1 = df.loc[name]
        for year in range(1955,1993):
            if '年份' in df1.columns:
                df1.set_index('年份',inplace=True)
            dirs = path+os.sep+name
            if not(os.path.exists(dirs)):
                os.makedirs(dirs)
            if year in df1.index:
                df2 = df1.loc[year]
            outpath = dirs+os.sep+dly+" "+name+str(year)+'.txt'
            df2.to_csv(outpath,index=None,header=0)
            print('successful {} {}'.format(name,year))
print("all successful")

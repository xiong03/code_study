# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:10:42 2022

@author: xiong
"""

import rasterio
import glob,os
import numpy as np
import pandas as pd

#求平均值
def fun(df_index,df):
    result_list = []
    for index in df_index.index:
        num = 0
        rows = df.iloc[index]
        for row in rows:
            num += row
        ave = num/rows.shape[0]
        print(ave)
        result_list.append(ave)
    return result_list

path = r"D:\python\雨量\2000"
tifs = glob.glob(path+os.sep+"*.tif")

with rasterio.open(tifs[1]) as scr:
    nodata = scr.nodata
    profile = scr.profile
    arr = scr.read(1)
arr[arr==nodata] = np.nan
arr = arr.reshape(-1,1)


for tif in tifs[2:]:
    with rasterio.open(tif) as scr1:
        arr1 = scr1.read(1)
    arr1[arr1==nodata] = np.nan
    temp = arr1.reshape(-1,1)
    arr = np.hstack([arr,temp])

df = pd.DataFrame(arr)
df_bool = pd.isnull(df).all(axis=1)
df_index = df_bool[df_bool==False]

result_list = fun(df_index,df)
df_list = pd.Series(result_list)
df_list.index = df_index.index
empty = pd.Series(np.full(36226560, np.nan))
com = empty.combine_first(df_list)
result = np.array(com).reshape(4717,7680)
outpath = r"D:\python\雨量\result\平均2000"
with rasterio.open(outpath , 'w', **profile) as Sre_write:
    Sre_write.write(result.astype(profile['dtype']), 1)

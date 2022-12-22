# -*- coding: utf-8 -*-
"""
Created on 2022-05-22 11:14:15

@author: Administrator
"""

import pandas as pd
import numpy as np
import rasterio
from glob import glob
from multiprocessing import Pool
import multiprocessing

def fun(row):
    num1 = 0
    for i in row:
        var = i**2
        num1 += var
    num2 = (row.sum())**(-1)
    num = num1*num2
    var = 0.1833*(num**1.9957)
    print(var)
    return var

files = glob(r"D:\python\雨量\2000\*tif")
with rasterio.open(files[1]) as src:    # 获取数据读取窗口
    profile = src.profile       #源数据的元信息集合（使用字典结构存储了数据格式，数据类型，数据尺寸，投影定义，仿射变换参数等信息）
    nodata = src.nodata
    df = src.read(1)
df[df==nodata] = np.nan
df = df.reshape(-1, 1)
for file in files[2:]:
    with rasterio.open(file) as src1:
        block_array = src1.read(1)    #产生二维数组
    block_array[block_array==nodata] = np.nan
    temp = block_array.reshape(-1, 1)
    df = np.hstack([df, temp])#追加每个月的dataframe
data = pd.DataFrame(df)
datat = pd.isnull(data).all(axis=1)
data1 = datat[datat==0]
list1 = []
for index in data1.index:
    row = data.iloc[index]
    num = fun(row)
    list1.append(num)
list2 = pd.Series(list1)
list2.index = data1.index
empty = pd.Series(np.full(36226560, np.nan))
com = empty.combine_first(list2)
com1 = np.array(com).reshape(4717, 7680)
out = r"D:\python\雨量\result\2020.tif"          #编写输出路径以及文件名
with rasterio.open(out , 'w', **profile) as Sre_write:#写出
    Sre_write.write(com1.astype(profile['dtype']), 1)
# cores = multiprocessing.cpu_count()                 # 计算机cpu的核心数（核心数=线程数，但具有多线程技术和超线程技术的线程数一般为核心数的两倍）
# pool = Pool(cores)                                  # 开启线程池



# num = pool.map(fun, data)


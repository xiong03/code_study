# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 21:05:11 2022

@author: xiong
"""

import rasterio
import pandas as pd
from tqdm import tqdm
from rasterio.enums import Resampling
import numpy as np

def fun(name):
    # 统计
    names = {}
    classify = r'C:\Users\xiong\Desktop\text\tif\int.tif'
    vgc = r'C:\Users\xiong\Desktop\text\tif\vgc.tif'

    # 分类
    with rasterio.open(classify) as scr1:
        arr1 = scr1.read(1)
        outmeta = scr1.meta.copy()
        scr1.close()
        scr1.close()
    del scr1

    # 植被碳
    with rasterio.open(vgc) as scr2:
        arr2 = scr2.read(out_shape=(1, outmeta['height'], outmeta['width']),
                          resampling=Resampling.nearest)[0]
        scr2.close()
    del scr2
    
    for i in name:
        names[str(i)] = np.nanmean(arr2[arr1==i])
    
    return names

tif = r'C:\Users\xiong\Desktop\text\result\new_text.tif'
csv = r'C:\Users\xiong\Desktop\text\temp\table.csv'
outfile = r'C:\Users\xiong\Desktop\text\result\new_result.tif'

# 统计
name = [6,7,9,10]
names = fun(name)

# 读取窗口和属性
with rasterio.open(tif) as scr:
    windows = [window for ij, window in scr.block_windows()]
    outmeta = scr.meta.copy()
    scr.close()
del scr


# 赋值
with rasterio.open(outfile, 'w', **outmeta) as dest:
    for win in tqdm(windows):
        with rasterio.open(tif) as scr:
            arr = pd.DataFrame(scr.read(1,window=win))
            # 将海洋变为0
            arr[arr==11] = 0
            # 给不同植被类型赋值
            for i in name:
                arr[arr==i] = names[str(i)]
            scr.close()
        del scr
        dest.write(arr,1,window=win)
        

# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 20:33:10 2022

@author: xiong
"""

import rasterio
import glob, os
import pandas as pd
import math
import numpy as np

path = r'C:\Users\xiong\Downloads\text'
outpath = r'D:\work\change'
files = glob.glob(path+os.sep+'*_1.tif')

# 降水
with rasterio.open(files[0]) as scr:
    arr = (scr.read(1)*100).astype('int16')+1
    outmeta = scr.meta.copy()
    scr.close()
del scr

outmeta.update({'dtype':'int16'})

with rasterio.open(outpath+os.sep+os.path.basename(files[0]), 'w', **outmeta) as dest:
    dest.write(arr,1)
    dest.close()
del dest, arr

# 气温
# with rasterio.open(files[1]) as scr:
#     df = pd.DataFrame((scr.read(1)-273.15).reshape(-1,1))
#     outmeta = scr.meta.copy()
#     scr.close()
# del scr

# df['pre'] = pd.DataFrame([abs(math.modf(i)[0]) for i in df[0]])
# df['pre'][df['pre']<0.5]=0
# df['pre'][df['pre']>0.5]=0.5
# df['result'] = df[0].astype('int8') + df['pre']
# arr = np.asarray(df['result']).astype('float32').reshape(outmeta['height'],outmeta['width'])

# outmeta.update({'dtype':'float32'})

# with rasterio.open(outpath+os.sep+os.path.basename(files[1]), 'w', **outmeta) as dest:
#     dest.write(arr,1)
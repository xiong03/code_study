# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 12:05:28 2022

@author: xiong
"""

import rasterio
import glob, os
import numpy as np

path = r'D:\0\text\data\地理数据云'
outpath = r'D:\0\text\result'
files = glob.glob(path+os.sep+'*.tif')
files = sorted(files,key = lambda i:len(i))

with rasterio.open(files[0]) as scr:
    outmeta = scr.meta.copy()
    # windows = [window for ij, window in scr.block_windows()]
    result = scr.read(1)
    scr.close()
del scr

i = 2
for file in files[1:]:
    
    # with rasterio.open(outpath+os.sep+'result.tif') as dest:
    
        # for win in windows:
    with rasterio.open(file) as scr:
        arr = scr.read(1)
        scr.close()
    del scr
    
    result = np.append(result,arr)
    result = result.reshape(i,arr.shape[0],arr.shape[1])
    if i<= len(files):
        i+=1
    else:
        i=len(files)
outmeta.update({'count':len(files)})
    
with rasterio.open(outpath+os.sep+'lj.tif', 'w', **outmeta) as dest:
    dest.write(result)
    
    
        
            
            
    
    
    
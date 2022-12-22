# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:27:04 2022

@author: xiong
"""

import rasterio
import glob, os

path = r'C:\Users\xiong\Downloads\out'
outpath = r'D:\0\text\result'

for file in glob.glob(path+os.sep+'*.tif'):
    
    outfile = outpath+os.sep+os.path.basename(file)
    
    with rasterio.open(file) as scr:
        arr = scr.read(1)
        outmeta = scr.meta.copy()
        scr.close()
    del scr
    
    outmeta.update({'nodata':0,'dtype':'int8'})
    
    with rasterio.open(outfile, 'w', **outmeta) as dest:
        dest.write(arr.astype(outmeta['dtype']),1)
        dest.close()
    del dest
    
    print(outfile)
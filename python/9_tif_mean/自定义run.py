# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:17:17 2022

@author: xiong
"""

import glob,os
import numpy as np
import threading
import rasterio
import traceback


class MyThread(threading.Thread):

    def __init__(self,func,args,name = ""):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name


    def run(self):
        self.func(*self.args)
  
def fun(path,year,outpath):
    files = glob.glob(path+os.sep+f'*{year}*.tif')
    
    with rasterio.open(files[0]) as scr1:
        temp_arr = scr1.read(1)
        profile = scr1.profile
        scr1.close()
    arr = temp_arr.reshape(-1,1)
    del temp_arr
    
    for file in files[1:]:
        with rasterio.open(file) as scr:
            temp_arr = scr.read(1)
            temp_arr = temp_arr.reshape(-1,1)
            scr.close()
        arr = np.hstack([arr,temp_arr])
        del temp_arr
        
    result = arr.mean(axis=1).reshape(profile['height'],profile['width'])
    with rasterio.open(outpath+os.sep+f'{year}.tif', 'w', **profile) as dest:
        dest.write(result.astype(profile['dtype']), 1)
        dest.close()
    print(f'successful {year}')
    

if __name__ == '__main__':
    threads = []
    path = r'D:\python\9_tif_mean\data\PDSI_MEAN'
    outpath = r'D:\python\9_tif_mean\result'
    for year in range(2000,2016):
        # fun(path,year,outpath)
        t = MyThread(fun, (path,year,outpath))
        threads.append(t)
        try:
            t.start()
        except:
            traceback.print_exc()
    for i in threads:
        t.join()
    

    
    
    

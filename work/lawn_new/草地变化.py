# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 20:45:16 2022

@author: xiong
"""

import glob
import os
import threading
import rasterio
import traceback
from tqdm import tqdm

class MyThread(threading.Thread):

    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(*self.args)


def fun(windows, file1, file2, outfile, outmeta):
    
    nums = [1,2,3,4,5,6,7,10,11,20,22,30,33,40,44,50,55,60,66,70,77]
    
    if os.path.exists(outfile):
        return
    
    with rasterio.open(outfile, 'w', **outmeta) as dest:
        for win in tqdm(windows):
            with rasterio.open(file1) as scr1:
                arr1 = scr1.read(1, window=win)
                scr1.close()
            del scr1

            with rasterio.open(file2) as scr2:
                arr2 = scr2.read(1, window=win)
                scr2.close()
            del scr2
            
            result = arr1*10+arr2

            for num in nums:
                result[result==num] = 0
            
            dest.write(result,1,window=win)
        dest.close()
    del dest
    
if __name__ == '__main__':
    path = r'D:\0\text\data'
    outpath = r'D:\0\text\result2'
    
    files = glob.glob(path+os.sep+'*.tif')
    with rasterio.open(files[0]) as scr:
        windows = [window for ij, window in scr.block_windows()]
        outmeta = scr.meta.copy()
        scr.close()
    del scr
    
    threads = []
    
    for i in range(len(files)-1):
        name1 = os.path.basename(files[i]).split('.')[0]
        name2 = os.path.basename(files[i+1]).split('.')[0]
        outfile = outpath+os.sep+f'{name1}-{name2}.tif'
        
        # fun(windows,files[i],files[i+1],outfile,outmeta)
        
        t = MyThread(fun, (windows,files[i],files[i+1],outfile,outmeta))
        threads.append(t)
        try:
            t.start()
        except:
            traceback.print_exc()
    for i in threads:
        t.join()
        
    
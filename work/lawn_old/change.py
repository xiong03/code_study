# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:37:26 2022

@author: xiong
"""

import glob,os
import numpy as np
import pandas as pd
import threading
import rasterio
import traceback
import time

class MyThread(threading.Thread):

    def __init__(self,func,args,name = ""):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name


    def run(self):
        self.func(*self.args)
        
def fun(path1,path2,outpath,windows):
    
    with rasterio.open(outpath, 'w', **outmeta) as dest:
    
        for win in windows:
            # start = time.time()
            
            with rasterio.open(path1) as scr1:
                temp1 = pd.DataFrame(scr1.read(1,window=win))
                scr1.close()
            del scr1
            
            with rasterio.open(path2) as scr2:
                temp2 = pd.DataFrame(scr2.read(1,window=win))
                scr2.close()
            del scr2
            
            if '30' not in path2:
                
                text = ((temp1.values>=31)&(temp1.values<=33) | (temp2.values>=31)&(temp2.values<=33))
            
            else:
                # 1到17 为草地资源图的栅格值
                text = ((temp1.values>=31)&(temp1.values<=33) | (temp2.values>=1)&(temp2.values<=17))
                # temp2.where((temp2.values>=1)&(temp2.values<=17),inplace=True)
            # text = (temp1.values>=11)&(temp1.values<=99)
            temp1.where(text, inplace=True)
            temp2.where(text, inplace=True)
            
            
            # 将小类归为大类
            for i in range(1,7):
                if i == 3:
                    continue
                temp1[(temp1>(i-1)*10) & (temp1<i*10)] == i*10
                if '30' not in path2:
                    temp2[(temp2>(i-1)*10) & (temp2<i*10)] == i*10
            
            # 去除无变化
            arr1 = temp1.copy()
            arr2 = temp2.copy()
            arr1[temp1==temp2] = np.nan
            arr2[temp1==temp2] = np.nan
            
            result = arr1.values.astype(outmeta['dtype'])*100+arr2.values.astype(outmeta['dtype'])
            
            dest.write(result, 1,window=win)
            
            # end = time.time()
            # print(end-start)
            
        dest.close()
    del dest
        
    
if __name__ == '__main__':
    threads = []
    path = r'D:\work\data'
    outpath = r'C:\Users\xiong\Desktop\result'
    # graph = r'D:\work\草地资源图\grass_china.tif'
    
    files = glob.glob(path+os.sep+'*.tif')
    
    with rasterio.open(files[0]) as scr:
        windows = [window for ij, window in scr.block_windows()]
        outmeta = scr.meta
        scr.close()
    del scr
    
    outmeta.update({'dtype':'int16'})
    
    for file1, file2 in zip(files[:-1], files[1:]):
        name1 = os.path.basename(file1).split('.')[0]
        name2 = os.path.basename(file2).split('.')[0]
        outfile = outpath+os.sep+name1+'_'+name2+'.tif'
        
        if os.path.exists(outfile):
            continue
        # start = time.time()
        # fun(file1, file2, outfile, windows)
        # end = time.time()
        # print(end-start)
        
        if os.path.exists(outfile):
            continue
        
        start = time.time()
        
        t = MyThread(fun, (file1,file2,outfile,windows))
        threads.append(t)
        try:
            t.start()
        except:
            traceback.print_exc()
    for i in threads:
        t.join()
    
    end = time.time()
    print(end-start)
    
    
    
    
    
    
    
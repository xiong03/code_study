# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 21:05:25 2022

@author: xiong
"""

import rasterio
import glob, os
import pandas as pd
import numpy as np
import threading
# import traceback
import time, math
from tqdm import tqdm

class MyThread(threading.Thread):

    def __init__(self,func,args,name = ""):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name


    def run(self):
        self.func(*self.args)

def fun(win,a):
    
    if a == 0:
        global result 
        result = pd.DataFrame(columns=x,index=y)
        result.replace(np.nan, 0, inplace=True)
    
    with rasterio.open(files[0]) as scr:
        pre = scr.read(1, window=win)
        scr.close()
    del scr
    
    with rasterio.open(files[1]) as scr:
        tem = scr.read(1, window=win)
        scr.close()
    del scr
    
    with rasterio.open(r'D:\work\草地资源图\clip.tif') as scr:
        grass = scr.read(1, window=win)
        scr.close()
    del scr
    
    if np.all(grass==0):
        return
    
    pre1 = pre[~np.isnan(pre)]
    tem1 = tem[~np.isnan(tem)]
    
    if len(pre1) != 0:
        temp_pre = np.unique(pre1.astype('int32'))
    if len(tem1) !=0:
        temp_tem = pd.DataFrame(np.unique(tem1))
        temp_tem['pre'] = pd.DataFrame([abs(math.modf(i)[0]) for i in temp_tem[0]])
        temp_tem['pre'][temp_tem['pre']<0.5]=0
        temp_tem['pre'][temp_tem['pre']>0.5]=0.5
        temp_tem['result'] = temp_tem[0].astype('int8') + temp_tem['pre']
        temp_tem = np.unique(temp_tem['result'])
    
    if len(pre1)!=0 and len(tem1)!=0:
        for value_p in tqdm(temp_pre):
            for value_t in temp_tem:
                # 将符合范围内的栅格数加上
                c = pd.DataFrame(grass[((pre>=value_p)&(pre<value_p+1))
                                    &((tem>=value_t)&(tem<value_t+0.5))&(grass!=0)]).count()
                result.loc[value_p,value_t] += c.values[0]
                
                # print(c.values[0])

    # temp_pre = np.unique(pre)
    # temp_tem = np.unique(tem)
    
    # for temp_y in tqdm(np.nditer(pre)):
    #     for temp_x in (np.nditer(tem)):
    #         result.loc[int(temp_y),float(temp_x)]+=1

        
            
    # print(a)

if __name__ == '__main__':
    
    start = time.time()
    
    path = r'D:\work\change\date_result\data_1'
    files = glob.glob(path+os.sep+'*.tif')
    
    with rasterio.open(r'D:\work\草地资源图\clip.tif') as scr:
        windows = [window for ij, window in scr.block_windows()]
        outmeta = scr.meta.copy()
        scr.close()
    del scr
    
    # 1-(10,7225), (-16,27) 351288
    # 2-(1,4900), (-26,27) 519294
    
    y = [i for i in range(10,7225,1)]
    x = [i for i in range(-16,27,1)]
    x.extend([i+0.5 for i in x])
    x = sorted(x)
    y = sorted(y)
    
    for a, win in enumerate(tqdm(windows)):
        fun(win,a)
    #     t = MyThread(fun, (win,a))
    #     threads.append(t)
    #     try:
    #         t.start()
    #         t.join()
    #     except:
    #         traceback.print_exc()
    
    result[result.values<=30] = 0
    
    data = pd.DataFrame(np.asarray(result).reshape(-1,1))
    data.columns = ['raster_quantity']
    data['temperature [°C]'] = x*len(y)
    data['precipitation [mm]'] = sorted((y*len(x)))
    data = data[data['raster_quantity']>30].copy()
    data.to_excel(r'D:\work\change\date_result\data_1'+os.sep+'result_1.xlsx',index=None)
    
    end = time.time()
    print(end-start)

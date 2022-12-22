# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 19:46:53 2022

@author: xiong
"""

import rasterio
import numpy as np
import glob, os
import time,math
from tqdm import tqdm
import pandas as pd

def fun(win,name):
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
    
    if not(np.any(grass==name)):
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
        for value_p in (temp_pre):
            for value_t in temp_tem:
                # 将符合范围内的栅格数加上
                c = pd.DataFrame(grass[((pre>=value_p)&(pre<value_p+1))
                                    &((tem>=value_t)&(tem<value_t+0.5))&(grass==name)]).count()
                result.loc[value_p,value_t] += c.values[0]
                
                # print(c.values[0])


if __name__ == '__main__':
    
    start = time.time()
    
    names = {'1':'温性草甸草原类','2':'温性草原类','3':'温性荒漠草原类','4':'高寒草甸草原类',
             '5':'高寒草原类','6':'高寒荒漠草原类','7':'温性草原化荒漠类','8':'温性荒漠类',
             '9':'高寒荒漠类','10':'热性草丛类','11':'热性灌草丛类','12':'暖性草丛类 ','17':'沼泽类',
             '13':'暖性灌草丛类','14':'低地草甸类','15':'温性山地草甸类','16':'高寒草甸类'}
    
    path = r'D:\work\change\date_result\data_2'
    files = glob.glob(path+os.sep+'*.tif')
    with rasterio.open(r'D:\work\草地资源图\clip.tif') as scr:
        windows = [window for ij, window in scr.block_windows()]
        scr.close()
    del scr
    
    for name in range(1,18):
        # 1-(10,7225), (-16,27) 351288
        # 2-(1,4900), (-26,27) 519294
        
        y = [i for i in range(1,4900,1)]
        x = [i-0.5 for i in range(-26,27,1)]
        x.extend([i+0.5 for i in x])
        x = sorted(x)
        y = sorted(y)
        
        result = pd.DataFrame(columns=x,index=y)
        result.replace(np.nan, 0, inplace=True)
        
        for win in tqdm(windows):
            fun(win,name)
            
        result[result.values<=30] = 0
        
        data = pd.DataFrame(np.asarray(result).reshape(-1,1))
        data.columns = ['raster_quantity']
        data['temperature [°C]'] = x*len(y)
        data['precipitation [mm]'] = sorted((y*len(x)))
        data = data[data['raster_quantity']>30].copy()
        data.to_excel(r'D:\work\change\date_result\classification_2'+os.sep+f'{names[str(name)]}_2.xlsx',index=None)
        
        end = time.time()
        print(end-start)
        print(f'successful {names[str(name)]}')
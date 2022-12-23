# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:42:08 2022

@author: xiong
"""

import ee

def ployinterp_column(region:ee.Geometry, List:list, num:int, default_value:int):
    """
    Parameters
    ----------
    region : ee.Geometry
        要处理的矢量范围
    List : list
        image放入list中
    num : int
        要进行插值的image数据为list中第几个
    default_value : int
        空值替换为该值
    """
    
    import traceback
    import pandas as pd
    import numpy as np
    from scipy.interpolate import lagrange
    import geemap
    import rasterio
    
    def ployinterp_column(s, n):
        List = list(range(0, n)) + list(range(n+1, len(s)))
        y = s.values[List] #取数，转换成列表
        List = np.array(List)[~np.isnan(y)]
        y = y[~np.isnan(y)] #剔除空值
        # print("List:{},y:{}".format(List,y))
        #print("表达式:{}".format(lagrange(List, y)))
        return lagrange(List, y)(n) #插值并返回插值结果，n是被插值的位置

    try:
        arr = geemap.ee_to_numpy(ee_object=List[0],region=region,default_value=default_value)
        result = pd.DataFrame(arr.reshape(-1,1))
        
        for image in List[1:]:
            arr_temp = geemap.ee_to_numpy(ee_object=image,region=region,default_value=default_value)
            arr_temp = arr_temp.reshape(-1,1)
            result = pd.concat([result,pd.DataFrame(arr_temp.reshape(-1,1))],axis=1)
        
        result_m = result.mean(axis=1).copy()
        result_s = np.std(np.array(result),axis=1)
        
        result_max = pd.DataFrame(result_m)+pd.DataFrame(result_s)*2
        result_min = pd.DataFrame(result_m)-pd.DataFrame(result_s)*2
        del result_m,result_s
        
        result.columns = [i for i in range(len(List))]
        
        r_handle = result[[num]].copy()
        
        for n, Max, Min, data in zip(result.index, result_max.values, result_min.values, r_handle.values):
            if (data[0] < Min[0]) or (data[0] > Max[0]) or (data[0] == default_value):
                r_handle.iloc[n,0] = default_value
                r_handle.iloc[n,0] = ployinterp_column(result.iloc[n],num)
        
        r_arr = np.array(r_handle).astype(type(List[0])).reshape(arr.shape[0],arr.shape[1])
        
        # return geemap.numpy_to_ee(np_array=r_arr,crs=List[0].projection().getInfo()['crs'],
        #                         transform=List[0].projection().getInfo()['transform'],
        #                         band_names=List[0].bandNames().getInfo())
        return r_arr

        print('successful')
    except:
        traceback.print_exc()
            
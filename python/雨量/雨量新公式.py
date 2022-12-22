# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:46:21 2022

@author: xiong
"""

import glob
from osgeo import gdal
import numpy as np
import time
import rasterio

path = r"D:\python\雨量\2000\pre2000.tif"
with rasterio.open(path) as scr:
    nodata = scr.nodata
    arr_p = scr.read(1)
arr_p[arr_p==nodata] = np.nan

#计算
def fun(arr,arr_p):
    arr_result = np.full((arr.shape[1],arr.shape[2]),np.nan)
    a,b,Fmod = [4.172,-152,0]
    for x in range(arr.shape[1]):
        for y in range(arr.shape[2]):
            for month in range(arr.shape[0]):
                if arr[month,x,y] == -32768:
                    break
                Fmod += (arr[month,x,y]**2)/arr_p[x,y]
            if Fmod != 0:
                arr_result[x,y] = a*Fmod+b
                print("x:{},y:{}".format(x,y))
    return arr_result

#整理数据                   
def fun1(path):
    tifs = glob.glob(path+"*.tif")
    months = range(13)
    arr = np.full((12,4717,7680),np.nan)
    for tif,month in zip(tifs[1:],months):
        dataset = gdal.Open(tif)
        #栅格矩阵的列数
        im_width = dataset.RasterXSize
        #栅格矩阵的行数
        im_height = dataset.RasterYSize
        #读取一个波段，其参数为波段的索引号，波段索引号从1开始
        band = dataset.GetRasterBand(1)
        #用ReadAsArray(<xoff>, <yoff>, <xsize>, <ysize>)读取整幅图像
        im_datas2 = band.ReadAsArray(0,0,im_width,im_height)
        #地图投影信息
        im_proj = dataset.GetProjection()
        #仿射矩阵，左上角像素的大地坐标和像素分辨率
        im_geotrans = dataset.GetGeoTransform()
        #将数据放入arr中
        arr[month, :, :] = im_datas2
    return arr,im_proj,im_geotrans,im_width,im_height,band

start = time.time()
path = r"E:\虚拟机\数据\2000/"
arr,im_proj,im_geotrans,im_width,im_height,band = fun1(path)
arr_result = fun(arr,arr_p)
#数组写入tif
outpath = r"E:\虚拟机\数据\result\PRE-2000.tif"
driver = gdal.GetDriverByName("GTiFF")
New_YG_dataset = driver.Create(outpath,im_width,im_height,1,gdal.GDT_Float64)
New_YG_dataset.SetProjection(im_proj)
New_YG_dataset.SetGeoTransform(im_geotrans)
#通过栅格的波段写入数据，result为数组形式的数据，行宽对应所创建文件的xy
band = New_YG_dataset.GetRasterBand(1) #将数据写入波段1中
band.WriteArray(arr_result)
end = time.time()
print('successful {}'.format(end-start))

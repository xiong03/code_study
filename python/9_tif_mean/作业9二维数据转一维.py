# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:41:30 2022

@author: xiong
"""
from osgeo import gdal
import numpy as np
import glob

def average(str1):
    path = r"D:\python\9_tif_mean\data\PDSI_MEAN"
    tifs = glob.glob(path+"\\"+"*.tif")
    df = []
    for tif in tifs:
        if str1 in tif:
            dataset = gdal.Open(tif)
            #栅格矩阵的列数
            im_width = dataset.RasterXSize
            #栅格矩阵的行数
            im_height = dataset.RasterYSize
            #地图投影信息
            im_proj = dataset.GetProjection()
            #仿射矩阵，左上角像素的大地坐标和像素分辨率
            im_geotrans = dataset.GetGeoTransform()
            #读取一个波段，其参数为波段的索引号，波段索引号从1开始
            band = dataset.GetRasterBand(1)
            #用ReadAsArray(<xoff>, <yoff>, <xsize>, <ysize>)读取整幅图像
            im_datas2 = band.ReadAsArray(0,0,im_width,im_height)
            #通过二维数据转一维来计算平均值
            im_datas1 = im_datas2.flatten()
            df.append(im_datas1)
    result = np.average(df,axis=0)
    result = result.reshape((im_height,im_width))
    result = result.astype(np.int32)
    return im_proj,im_geotrans,im_width,im_height,result

for str1 in range(2000,2016):
    im_proj,im_geotrans,im_width,im_height,result = average(str(str1))
    path = r"D:\python\9_tif_mean\result"
    outpath = path+"\\"+str(str1)+".tif"
    driver = gdal.GetDriverByName("GTiFF")
    New_YG_dataset = driver.Create(outpath,im_width,im_height,1,gdal.GDT_Int32)
    New_YG_dataset.SetProjection(im_proj)
    New_YG_dataset.SetGeoTransform(im_geotrans)
    band = New_YG_dataset.GetRasterBand(1)
    band.WriteArray(result)
    print("successful {}".format(str1))

del result
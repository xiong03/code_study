# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:02:48 2021

@author: 树风
"""
import scipy.stats as st
import os
from multiprocessing import Pool     #pool:赋予函数并行化处理一系列输入值的能力，可以将输入数据分配给不同进程处理（数据并行）
import multiprocessing               #多进程进行的库，基于进程的并行
from osgeo import gdal               #栅格数据用的库
import numpy as np      
import pandas as pd          

data_2 = np.arange(2000, 2016, 1)        # 计算趋势与显著性水平所需的年份，fun1中引用  

def fun1(data_1):           
    """                     
    param data_1: 需要计算趋势和显著性水平的数组           
    return: 返回趋势r2score和显著性水平pvalue      
    """      
    y_data = data_1                             #因变量
    x_data = data_2                             #自变量
    y_data = y_data.reshape(-1, 1)              #重塑数组  1列，n行
    slope, intercept, r_value, p_value, std_err = st.linregress(x_data, y_data)             
    return slope, p_value                          # 返回显著性水平和趋势                  

if __name__ == '__main__':     
    tif1 = r'C:\Users\树风\Desktop\MAT\t2000.tif'                            # 需要读取的tif文件所在的文件夹的所在文件夹的路径    
    ds = gdal.Open(tif1)                             # 打开文件
    im_width = ds.RasterXSize                           # 获取栅格矩阵的列数
    print(im_width)
    im_height = ds.RasterYSize                          # 获取栅格矩阵的行数
    print(im_height)
    im_bands = ds.RasterCount                           # 获取栅格矩阵的波段数
    print(im_bands)
    band1 = ds.GetRasterBand(1)                         # 波段的indice起始为1，不为0
    img_datatype = band1.DataType                       # 数据类型
    data1 = np.full((16, im_height * im_width), 1.0)    # 建立数组
    for year in range(2000, 2016):
        path = r'C:\Users\树风\Desktop\MAT'
        file2 = path + os.sep + 't' + str(year) +'.tif'
        ds = gdal.Open(file2)                           #打开栅格数据
        img_data = ds.ReadAsArray()                     # 读取整幅图像转化为数组
        img_data = img_data.reshape(1, -1)              # 将数组转化为1行，自定义列的数组
        data1[year - 2000] = img_data                   # 将读取的数组合并成一个大的数组    # 将数组转换成以象元数为列数，年份为行数的数组
    data1 = pd.DataFrame(data1).T                   # 数组转化为dataframe，并进行 行列互换
    data1 = data1.values                            # dataframe转化为数组    
    cores = multiprocessing.cpu_count()                 # 计算机cpu的核心数（核心数=线程数，但具有多线程技术和超线程技术的线程数一般为核心数的两倍）
    print(cores)
    pool = Pool(cores)                                  # 开启线程池
    data2 = pool.map(fun1, data1)                       # 进行并行计算，得到的data2是一个列表，map是按行读取数组来计算
    data2 = pd.DataFrame(data2)
    data2 = data2.values                      # 将data2转换成对应数组
    data3 = data2[:, 0]
    data4 = data2[:, 1]
    data3 = data3.reshape(im_height, im_width)
    data4 = data4.reshape(im_height, im_width)        # 写入文件
    var = [r'MAT趋势1.tif',r'MAT显著性水平2.tif']    
    datas = [data3,data4]
    for j in range(0,2):
        driver = gdal.GetDriverByName('GTiff')                  # 获取数据驱动者名  （why)
        out_ds = driver.Create(
            r'C:\Users\树风\Desktop/' + var[j],                   # tif文件所保存的路径
        ds.RasterXSize,                                     # 获取栅格矩阵的列数
        ds.RasterYSize,                                     # 获取栅格矩阵的行数
        ds.RasterCount,                                     # 获取栅格矩阵的波段数
        img_datatype)                                       # 获取第一波段的数据类型
        out_ds.SetProjection(ds.GetProjection())                # 投影信息
        out_ds.SetGeoTransform(ds.GetGeoTransform())            # 仿射信息
        for i in range(1, ds.RasterCount + 1):                  # 循环逐波段写入
            out_band = out_ds.GetRasterBand(i)
            out_band.WriteArray(datas[j])                           # 写入数据 (why)
        out_ds.FlushCache()  #(刷新缓存)
        del out_ds #删除     
    

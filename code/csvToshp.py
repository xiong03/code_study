# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:14:57 2022

@author: xiong
"""

import os
from osgeo import ogr
import pandas as pd
from osgeo import osr
import glob

# 将坐标转为shp点
def fun(csv_file:str, shp_path:str, csr=4326):
    """

    Parameters
    ----------
    csv_filename : str
        csv文件的路径
        格式为station latitude longitude
    shp_filename : str
        shp保存的路径(不包括shp数据名字,自动与csv数据名字相同)
    csr : int
        地理坐标的编码（默认为wgs84）

    Returns
    -------
    shp数据

    """
    # 读入csv文件信息，设置点几何的字段属性
    csv_df = pd.read_csv(csv_file)

    # 利用.csv文件创建一个点shp文件
    
    # 获取驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    # 创建数据源
    shp_filename = os.path.basename(csv_file).split('.')[0] + '.shp'
    # 检查数据源是否已存在
    if os.path.exists(os.path.join(shp_path, shp_filename)):
        driver.DeleteDataSource(os.path.join(shp_path, shp_filename))    
    ds = driver.CreateDataSource(os.path.join(shp_path, shp_filename))
    
    # 图层名
    layer_name = os.path.basename(csv_file).split('.')[0]
    
    # 定义坐标系对象
    sr = osr.SpatialReference()
    # 使用WGS84地理坐标系
    sr.ImportFromEPSG(csr)
    
    # 创建点图层, 并设置坐标系
    out_lyr = ds.CreateLayer(layer_name, srs = sr, geom_type=ogr.wkbPoint)
    
    # 创建图层定义
    # 利用csv文件中有三个字段创建3个属性字段
    # station字段
    # 如果有其他字段，可在此处添加
    station_fld = ogr.FieldDefn('station', ogr.OFTString)
    station_fld.SetWidth(6)
    out_lyr.CreateField(station_fld)
    # Latitude字段
    lat_fld = ogr.FieldDefn('latitude', ogr.OFTReal)
    lat_fld.SetWidth(9)
    lat_fld.SetPrecision(5)
    out_lyr.CreateField(lat_fld)
    # Longitude字段
    lon_fld = ogr.FieldDefn('longitude', ogr.OFTReal)
    lon_fld.SetWidth(9)
    lon_fld.SetPrecision(5)
    out_lyr.CreateField(lon_fld)
    
    featureDefn = out_lyr.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    
    # 设定几何形状
    point = ogr.Geometry(ogr.wkbPoint)
    
    # 读入csv文件信息，设置点几何的字段属性
    for i in range(len(csv_df)):
        
        # 设置属性值部分
        # 站点Id
        feature.SetField('station', str(csv_df.iloc[i, 0]))
        # 纬度
        feature.SetField('latitude', float(csv_df.iloc[i, 1]))
        # 经度
        feature.SetField('longitude', float(csv_df.iloc[i, 2]))

        
        # 设置几何信息部分
        # 利用经纬度创建点， X为经度， Y为纬度
        point.AddPoint(float(csv_df.iloc[i, 2]), float(csv_df.iloc[i, 1]))
        feature.SetGeometry(point)
        
        # 将feature写入layer
        out_lyr.CreateFeature(feature)
    
    # 从内存中清除 ds，将数据写入磁盘中
    ds.Destroy()
    print('successful '+csv_file)
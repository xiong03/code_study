# -*- coding: utf-8 -*-
import os
import arcpy
from arcpy.sa import *
import sys
import pandas as pd
import random

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

reload(sys)
sys.setdefaultencoding("utf-8")

polygon = r'C:\Users\xiong\Desktop\text\shp\new_polygon.shp'
VGC = r'C:\Users\xiong\Desktop\text\shp\VGC.shp'
classify = r'C:\Users\xiong\Desktop\text\tif\result.tif'
primeval = r'C:\Users\xiong\Desktop\text\tif\vgc.tif'
temp = r'C:\Users\xiong\Desktop\text\temp'
result = r'C:\Users\xiong\Desktop\text\result'

# 复制要素
print('CopyFeatures')
arcpy.management.CopyFeatures(VGC, temp+os.sep+'VGC.shp')
arcpy.management.CopyFeatures(polygon, temp+os.sep+'new_polygon.shp')

print('MakeFeatureLayer_management')
# 创建要素图层
arcpy.MakeFeatureLayer_management(temp+os.sep+'new_polygon.shp', "polygon")
arcpy.MakeFeatureLayer_management(temp+os.sep+'VGC.shp', 'VGC')

print('AddField_management')
# 添加字段
arcpy.AddField_management('polygon', 'mean', 'FLOAT')
arcpy.AddField_management('VGC', 'vgc', 'FLOAT')

print('CalculateField_management')
# 计算字段
arcpy.CalculateField_management('VGC', 'vgc', '[植被碳_]')

print('TabulateIntersection_analysis')
# 交集制表
arcpy.TabulateIntersection_analysis('polygon', 'FID', 'VGC', temp+os.sep+'table.csv', '', 'vgc')

print('AddJoin')
# 添加关联
arcpy.management.AddJoin('polygon', 'FID', temp+os.sep+'table.csv', 'FID')

print('CalculateField_management')
# 计算字段
arcpy.CalculateField_management('polygon', 'mean', '[table.csv.vgc]/ [table.csv.PNT_COUNT]')

# 获取table中的mean
mean = []
with arcpy.da.UpdateCursor(temp+os.sep+'new_polygon.shp', 'mean') as cursor:
    for row in cursor:
        if row != 0.0:
            mean.append(row[0])

# 将polygon中为0的数据随机获取table中的数据
with arcpy.da.UpdateCursor(temp+os.sep+'new_polygon.shp', 'mean') as cursor:
    for row in cursor:
        num = random.randint(0, len(mean)-1)
        if row[0] == 0.0:
            row[0] = mean[num]*random.uniform(0, 1)
            cursor.updateRow(row)

print('PolygonToRaster_conversion')
# 面转栅格
arcpy.PolygonToRaster_conversion('polygon', 'mean', temp+os.sep+'polygon.tif', '', '', 30)

# print('Resample')
# # 重采样
# arcpy.management.Resample(temp+os.sep+'polygon.tif', temp+os.sep+'polygon_30.tif', '30 30', 'NEAREST')
# arcpy.management.Resample(primeval, temp+os.sep+'vgc_30.tif', '30 30', 'MAJORITY')

print('Con')
# 条件函数
outCon = Con(Raster(classify), temp+os.sep+'polygon.tif', Raster(classify), 'VALUE<=5')
# outCon = Con(Raster(classify), temp+os.sep+'polygon_30.tif', Con(Raster(classify), Raster(classify), temp+os.sep+'vgc.tif', 'VALUE=11'), 'VALUE<=5')
outCon.save(result+os.sep+'new_text.tif')


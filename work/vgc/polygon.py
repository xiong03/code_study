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
arcpy.env.parallelProcessingFactor = 0

fishnet = r'C:\Users\xiong\Desktop\text\shp\fishnet.shp'
tif = r'C:\Users\xiong\Desktop\text\tif\result.tif'
temp = r'C:\Users\xiong\Desktop\text\temp'

# 复制要素
print('CopyFeatures')
arcpy.management.CopyFeatures(fishnet, temp+os.sep+'fishnet.shp')

# 缓冲区
print('Buffer_analysis')
arcpy.Buffer_analysis(temp+os.sep+'fishnet.shp', temp+os.sep+'fishnet_buffer.shp', '3000 Meters')

# 生成随机点
print('CreateRandomPoints')
arcpy.management.CreateRandomPoints(temp, 'point', temp+os.sep+'fishnet_buffer.shp', '', 200, '500 Meters')

# 添加xy坐标
print('AddXY_management')
arcpy.AddXY_management(temp+os.sep+'point.shp')

# 通过CID字段(通过游标获取CID字段)来筛选对应范围的
CID = []
with arcpy.da.SearchCursor(temp+os.sep+'point.shp', ['CID']) as cursor:
    for row in cursor:
        if row[0] not in CID:
            CID.append(row[0])

# 按属性选择要素
print('SelectLayerByAttribute_management')
for id in CID:
    # 创建要素图层
    print('MakeFeatureLayer_management')
    arcpy.MakeFeatureLayer_management(temp+os.sep+'point.shp', "point")

    # 按属性选择
    print('SelectLayerByAttribute_management')
    arcpy.SelectLayerByAttribute_management('point', 'NEW_SELECTION', '"CID"={}'.format(id))

    # 点集转线
    print('PointsToLine')
    if id <= 13:  # 横向连接
        arcpy.management.PointsToLine('point', temp+os.sep+'temp_{}.shp'.format(id), '', 'POINT_X')
    else:
        arcpy.management.PointsToLine('point', temp+os.sep+'temp_{}.shp'.format(id), '', 'POINT_Y')

inputs = [temp+os.sep+'temp_{}.shp'.format(i) for i in CID]
# 合并
print('Merge_management')
arcpy.Merge_management(inputs, temp+os.sep+'line.shp')

# 延申线
print('ExtendLine_edit')
arcpy.ExtendLine_edit(temp+os.sep+'line.shp')

# 要素转面
print('FeatureToPolygon')
arcpy.management.FeatureToPolygon(temp+os.sep+'line.shp', temp+os.sep+'polygon.shp')
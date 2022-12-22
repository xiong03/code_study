# -*- coding: utf-8 -*-
import os
import arcpy
from arcpy.sa import *
import sys

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = 0

reload(sys)
sys.setdefaultencoding("utf-8")

# 随机点的个数
count = 1000
shp = r'D:\work\new\矢量\03青海湖流域草地资源.shp'
shp = unicode(shp, 'utf-8')
outpath = r'D:\work\new\point'
temp = r'D:\work\new\temp'
prj = r'C:\Users\xiong\Documents\geemap\shp\jxwgs\jx.prj'
landuse = "CY_L"

# 复制要素
print('CopyFeatures')
arcpy.management.CopyFeatures(shp, temp+os.sep+u'草地.shp')

# 草地类型
CY_L = []
with arcpy.da.SearchCursor(temp+os.sep+u'草地.shp', [landuse]) as cursor:
    for row in cursor:
        if row[0] not in CY_L:
            CY_L.append(row[0])
del cursor

# 添加字段
print('AddField_management')
arcpy.AddField_management(temp+os.sep+u'草地.shp', 'num', 'LONG')

# 对类型进行分类num
with arcpy.da.UpdateCursor(temp+os.sep+u'草地.shp', [landuse, 'num']) as cursor:
    for row in cursor:
        for i, cy in enumerate(CY_L):
            if row[0] == cy:
                row[1] = i+1
                cursor.updateRow(row)
del cursor

# 融合
print('Dissolve')
arcpy.management.Dissolve(temp+os.sep+u'草地.shp', temp+os.sep+'dissolve.shp', ['num'], '', '', "DISSOLVE_LINES")

num = []
# 判断融合之后的要素个数
with arcpy.da.SearchCursor(temp+os.sep+'dissolve.shp', ['FID', 'num']) as cursor:
    for row in cursor:
        FID = row[0]
        num.append(row[1])

# 创建随机点
print('CreateRandomPoints')
arcpy.management.CreateRandomPoints(temp, 'all.shp', temp+os.sep+'dissolve.shp', '', count/FID, '500 Meters')

# 投影
print('Project_management')
arcpy.Project_management(temp+os.sep+'all.shp', outpath+os.sep+'all.shp', prj)

with arcpy.da.UpdateCursor(outpath+os.sep+'all.shp', ['CID']) as cursor:
    for row in cursor:
        for FID, i in enumerate(num):
            if row[0] == FID:
                row[0] = num[FID]
        cursor.updateRow(row)
del cursor

# print(CY_L)
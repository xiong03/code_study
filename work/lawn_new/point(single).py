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
count = 50
shp = r'D:\work\new\矢量\11青海湖流域土地利用现状.shp'
shp = unicode(shp, 'utf-8')
outpath = r'D:\work\new\point'
temp = r'D:\work\new\temp'
prj = r'C:\Users\xiong\Documents\geemap\shp\jxwgs\jx.prj'
landuse = "DLMC"

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

# 添加字段
print('AddField_management')
arcpy.AddField_management(temp+os.sep+u'草地.shp', 'id', 'LONG')

# 对类型进行分类num
with arcpy.da.UpdateCursor(temp+os.sep+u'草地.shp', [landuse, 'num', 'id']) as cursor:
    for row in cursor:
        for i, cy in enumerate(CY_L):
            if row[0] == cy:
                row[1] = i+1+7
                row[2] = 0
                cursor.updateRow(row)
del cursor

num = []
with arcpy.da.SearchCursor(temp+os.sep+u'草地.shp', ['num']) as cursor:
    for row in cursor:
        if row[0] not in num:
            num.append(row[0])
del cursor

for i, cy in zip(num, CY_L):
    # 创建要素图层
    print('MakeFeatureLayer_management')
    arcpy.MakeFeatureLayer_management(temp + os.sep + u'草地.shp', u"草地")

    # 按属性选择
    print('SelectLayerByAttribute_management')
    arcpy.SelectLayerByAttribute_management(u"草地", 'NEW_SELECTION', '"num"={}'.format(i))

    # 融合
    print('Dissolve')
    arcpy.management.Dissolve(u'草地', temp+os.sep+u'{}.shp'.format(cy+'{}'.format(i)), ['id'], '', '', "DISSOLVE_LINES")

    # 判断融合之后的要素个数
    with arcpy.da.SearchCursor(temp + os.sep + u'{}.shp'.format(cy + '{}'.format(i)), ['FID']) as cursor:
        for row in cursor:
            FID = row[0]+1

    # 创建随机点
    print('CreateRandomPoints')
    arcpy.management.CreateRandomPoints(temp, u'{}.shp'.format(cy), temp+os.sep+u'{}.shp'.format(cy+'{}'.format(i)), '', count/FID, '30 Meters')

    # 投影
    print('Project_management')
    arcpy.Project_management(temp+os.sep+u'{}.shp'.format(cy), outpath+os.sep+'{}.shp'.format(i), prj)

    with arcpy.da.UpdateCursor(outpath+os.sep+'{}.shp'.format(i), ['FID', 'CID']) as cursor:
        for row in cursor:
            row[1] = row[0]
            cursor.updateRow(row)

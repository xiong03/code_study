# -*- coding: utf-8 -*-
import os
import glob
import arcpy
from arcpy.sa import *
import sys

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

reload(sys)
sys.setdefaultencoding("utf-8")

mxd_path = r'D:\0\text\template.mxd'
path = r'D:\0\text\result2'
outpath = r'D:\0\text\jpg'
tifs = glob.glob(path+os.sep+'*.tif')

for tif in tifs:
    name = os.path.basename(tif).split('.')[0]
    outfile = outpath+os.sep+'{}.jpg'.format(name)

    if os.path.exists(outfile):
        continue

    # 加载地图文档
    mxd = arcpy.mapping.MapDocument(mxd_path)

    # 调出“图层”数据框
    layer = arcpy.mapping.ListDataFrames(mxd, "layers")[0]

    # 在数据框下的所有图层
    lyrs = arcpy.mapping.ListLayers(mxd, "", layer)

    for lyr in lyrs:
        lyr.replaceDataSource(path, "RASTER_WORKSPACE", name)

        title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[1]
        title.text = "%s年西藏地区草地类型转换空间分布" % name

    # 刷新地图和布局窗口
    arcpy.RefreshActiveView()
    # 刷新内容列表
    arcpy.RefreshTOC()
    # 输出
    arcpy.mapping.ExportToTIFF(mxd, outfile, resolution=500)
    del mxd
    print(outfile)



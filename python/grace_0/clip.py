# coding:utf-8
import arcpy
import os
import sys
import pandas as pd
from arcpy.sa import *
reload(sys)
sys.setdefaultencoding("utf-8")
arcpy.CheckOutExtension("spatial")
arcpy.gp.overwriteOutput = True

data_names = ["MINIMUM", "MAXIMUM", "MEAN", "STD"]
result = pd.DataFrame(columns=["name", "MINIMUM", "MAXIMUM", "MEAN", "STD"])
path = r"D:\python\grace_0\grace"
clip_features = r"D:\python\grace_0\range\polygon.shp"
outpath = r"D:\python\grace_0\out"  # excel
output_path = r"D:\python\grace_0\result"  # 裁剪结果
for year in range(2002, 2018):
    names = os.listdir(path+os.sep+str(year))
    for name in names:
        name1 = name.split('.')[0]
        name2 = name.split('.')[-2].split('_')[-1]
        data = pd.DataFrame(columns=['name'])
        in_raster = path + os.sep + str(year) + os.sep + name
        out_raster = outpath + os.sep + name
        if '.tif' not in in_raster:
            continue
        arcpy.Clip_management(in_raster, '#', out_raster, clip_features, '32767', "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        #  替换栅格值
        # arcpy.env.workspace = "D:\python\grace_0\out"
        # rasterlist = arcpy.ListRasters("*", "tif")
        # for raster in rasterlist:
        #     out = output_path + os.sep + raster
        #     outCon = Con(Raster(raster) >= 32760, 0, raster)
        #     outCon.save(out)
        # print("sucessful {}".format(name1 + "-" + name2))
        #  获取数据
        for data_name in data_names:
            data1 = arcpy.GetRasterProperties_management(out_raster, data_name)
            data.insert(len(data.columns), data_name, data1)
            print("successful {}".format(name1 + "-" + name2))
        data['name'] = name1 + "-" + name2
        result = pd.concat([result, data])
    print("successful {}".format(year))
result.to_excel(r"D:\python\grace_0\out.xls", header=True, index=False, float_format='%.1f')
print('all successful')
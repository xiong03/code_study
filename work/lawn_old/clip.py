# coding:utf-8
import arcpy
import glob, os
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
arcpy.CheckOutExtension("spatial")
# 如果文件已存在就覆盖
arcpy.env.overwriteOutput = True


path = r'D:\work\china_lucc'
outpath = r'D:\work\result'
shp = r'D:\work\shp\Land_reclamation_China\China_reclamation_region_1985_2020.shp'
files = glob.glob(path+os.sep+'*'+os.sep+'*.tif')

for file in files:
    name = os.path.basename(file)
    outfile = outpath + os.sep + name

    # 裁剪
    arcpy.Clip_management(file, '#', outfile, shp, '255', "#", "NO_MAINTAIN_EXTENT")

    print('successful {}'.format(name))
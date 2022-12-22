# coding:utf-8
import arcpy
from arcpy.sa import *
import pandas as pd
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")

# Set environment settings
arcpy.env.workspace = "C:/data"

# Set local variables
inRaster = "D:\望勇数据\《自然地理学》补充课程\soil\腾冲边界线\soil_1km1_1954.tif"
outPolygons = "D:\望勇数据\《自然地理学》补充课程\soil\result\soil1954.shp"
field = "VALUE"

# Execute RasterToPolygon
arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "SIMPLIFY", field)

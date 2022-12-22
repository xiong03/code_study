# -*- coding: utf-8 -*-
import glob, os
import arcpy
from arcpy.sa import *
import sys

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = 0

reload(sys)
sys.setdefaultencoding("utf-8")

path = r'C:\Users\xiong\Downloads\out'
temp = r'D:\0\text\temp'
outpath = r'D:\0\text\data'

for year in range(1985, 2020, 5):
    files = glob.glob(path+os.sep+'{}*.tif'.format(year))

    if len(files) == 0 or os.path.exists(outpath+os.sep+'{}.tif'.format(year)):
        continue

    # print('SetNull')
    # out_raster1 = SetNull(files[0], files[0], 'VALUE = 0')
    # out_raster2 = SetNull(files[1], files[1], 'VALUE = 0')

    print('MosaicToNewRaster_management')
    arcpy.MosaicToNewRaster_management('{};{}'.format(files[0], files[1]), temp, '{}.tif'.format(year), '', '8_BIT_SIGNED', '', '1')

    print('CopyRaster')
    arcpy.management.CopyRaster(temp+os.sep+'{}.tif'.format(year), outpath+os.sep+'{}.tif'.format(year), nodata_value=0)

    print(year)
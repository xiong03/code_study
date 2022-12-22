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
landuse = r''
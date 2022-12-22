# -*-*- coding: utf-8 -*
import arcpy
import os, glob
import sys
from arcpy.sa import *

# 编码转换
reload(sys)
sys.setdefaultencoding('utf-8')
arcpy.CheckOutExtension("Spatial")
# 如果文件已存在就覆盖
arcpy.env.overwriteOutput = True

path = r'D:\work\change\tif'
outpath = r'C:\Users\xiong\Desktop\result\tif'

for file in glob.glob(path+os.sep+'*.tif'):

    outfile = outpath+os.sep+os.path.basename(file)

    if '30' in outfile or os.path.exists(outfile):
        continue

    # 设为空函数
    outSetNull = SetNull(file, file, 'Value=3131 OR Value=3232 OR Value=3333')
    outSetNull.save(outfile)

    print('successful {}'.format(outfile))


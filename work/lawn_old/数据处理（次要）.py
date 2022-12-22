# coding:utf-8
import arcpy
import glob
import os
import sys
import numpy as np
import pandas as pd
import re

reload(sys)
sys.setdefaultencoding("utf-8")
arcpy.CheckOutExtension("spatial")
# 如果文件已存在就覆盖
arcpy.env.overwriteOutput = True

# 主要任务为将栅格值改为文字

path = r'D:\work\change\result'
outpath = r'C:\Users\xiong\Desktop\result'
files = glob.glob(path+os.sep+'*.tif')

# # 字段代码
# codeblock = '''
# def funcation(Value):
#     str1 = str(Value)[:2]
#     str2 = str(Value)[2:]
#
#     if str1.startswith('1'):
#         name1 = '耕地'
#     elif str1.startswith('2'):
#         name1 = '林地'
#     elif str1.startswith('3'):
#         name1 = '草地'
#     elif str1.startswith('4'):
#         name1 = '水域'
#     elif str1.startswith('5'):
#         name1 = '建筑用地'
#     else:
#         name1 = '未利用地'
#
#     if str2.startswith('1'):
#         name2 = '耕地'
#     elif str2.startswith('2'):
#         name2 = '林地'
#     elif str2.startswith('3'):
#         name2 = '草地'
#     elif str2.startswith('4'):
#         name2 = '水域'
#     elif str2.startswith('5'):
#         name2 = '建筑用地'
#     else:
#         name2 = '未利用地'
#
#     return name1+'->'+name2
# '''

# 字段代码
codeblock = '''
def funcation(Value):
    str1 = str(Value)[:2]
    str2 = str(Value)[2:]
    
    if str1.startswith('3'):
        name1 = '草地'
    else:
        name1 = '非草地'
    
    if str2.startswith('3'):
        name2 = '草地'
    else:
        name2 = '非草地'
    
    if name1 == name2:
        return '无变化'
    else:
        return name1+'->'+name2
    
'''

for in_raster in files:

    outfile = outpath + os.sep + os.path.basename(in_raster)

    if os.path.exists(outfile):
        continue

    print('MakeRasterLayer')
    # 栅格转图层
    arcpy.management.MakeRasterLayer(in_raster, 'layer')

    print('AddField')
    # 添加字段
    arcpy.management.AddField('layer', 'change', 'TEXT', '20')

    print('CalculateField_management')
    # 字段计算器
    arcpy.CalculateField_management('layer', 'change', 'funcation(!Value!)', 'PYTHON_9.3', codeblock)

    print('CopyRaster_management')
    # 复制栅格
    arcpy.CopyRaster_management('layer', outfile)

    # print('RemoveLayer')
    # # 删除图层
    # arcpy.mapping.RemoveLayer('layer')

    print('successful {}'.format(outfile))

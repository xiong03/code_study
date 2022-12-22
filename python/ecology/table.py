# coding:utf-8
import arcpy
import glob
import os
import sys
import numpy as np
import pandas as pd

reload(sys)
sys.setdefaultencoding("utf-8")
arcpy.CheckOutExtension("spatial")

# 获取所有数据中的LNAME字段
def get_flied(outpath):
    # z盘数据
    path_data = r"Z:\00.生态修复\上饶广信区数据\22个乡镇总体规划数据\22个乡镇总体规划数据/"
    path_data = unicode(path_data, 'utf-8')

    temp_list = []
    # 文件下的文件名
    dirs = os.listdir(path_data)
    for dir1 in dirs:

        if dir1 == u'上饶物流园土地使用规划图':
            continue

        study_areas = glob.glob(path_data + dir1 + os.sep + "*.shp")

        for study_area in study_areas:

            # 存放LNAME字段的变量
            flied = 'LNAME'
            cursor = arcpy.SearchCursor(study_area, fields=flied)
            for row in cursor:
                temp_list.append(row.LNAME)
            temp_df = pd.DataFrame(np.unique(temp_list))
    temp_df.to_excel(outpath, index=False)
    print('sucessful')

# 调试
outpath = r"D:\ecology/"
get_flied(outpath+'class.xls')
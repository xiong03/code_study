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
# 设置字段限制
arcpy.env.qualifiedFieldNames = False


# 中间数据存放shp/tif
shp_temp = r"D:\ecology\temp\shp"
tif_temp = r"D:\ecology\temp\tif"

# 研究区shp
# data_study_area = r"D:\ecology\data/"
path_data = r"D:\ecology\data"
path_data = unicode(path_data, 'utf-8')

# 森林公园数据
data_forest = r"D:\ecology\江西省\forsets"
data_forest = unicode(data_forest, 'utf-8')

# 道路数据shp
data_road = r"D:\ecology\江西省\市区道路_2000.shp"
data_road = unicode(data_road, 'utf-8')

# 铁路数据shp
data_railway = r"D:\ecology\江西省\铁路_2000.shp"
data_railway = unicode(data_railway, 'utf-8')

# 高速数据shp
data_freeway = r"D:\ecology\江西省\高速_2000.shp"
data_freeway = unicode(data_freeway, 'utf-8')

# 河流数据shp
data_river = r"D:\ecology\江西省\常年湖_2000.shp"
data_river = unicode(data_river, 'utf-8')

def start_(str1):
    print("Processing: " + str1 + '\t')


def end_(str2):
    print(str2 + '\t' + 'is ok------' + '\t')

# 对高速等数据的处理
def fun(data, study_area, name, field, cell, distance, control=True):

    """"
    :param data: 河流，高速等shp数据
    :param study_area: 研究区
    :param name: 研究区的名字
    :param field: 字段值(int)
    :param cell: 像元值(int)
    :param distance: 缓冲区距离(int)
    :param control: 用于控制是否生成缓冲区，默认为生成（True）
    :return: tif数据路径
    """

    # 裁剪
    shp_name = shp_temp+os.sep+name+'.shp'
    arcpy.Clip_analysis(data, study_area, shp_name)

    # 如何数据没用相加，退出函数
    if arcpy.management.GetCount(shp_name)[0] == "0":
        print('fail to {}'.format(name))
        return -1

    # 添加字段
    arcpy.AddField_management(shp_name, 'coast', 'FLOAT')

    # 计算字段
    arcpy.CalculateField_management(shp_name, 'coast', field, 'VB')

    # 生成缓冲区(河流不需要生成)
    if control:
        buffer_shp = shp_temp+os.sep+name+'_buffer.shp'
        arcpy.Buffer_analysis(shp_name, buffer_shp, str(distance)+' Meters', 'FULL', 'ROUND', 'NONE')

        # 添加字段
        arcpy.AddField_management(buffer_shp, 'coast', 'FLOAT')

        # 计算字段
        arcpy.CalculateField_management(buffer_shp, 'coast', field, 'VB')

        # 面转栅格
        tif_name = tif_temp+os.sep+name+'.tif'
        arcpy.PolygonToRaster_conversion(buffer_shp, 'coast', tif_name, 'CELL_CENTER', 'NONE', cell)

        print('successful {}'.format(name))

        # 返回tif数据的路径
        return tif_name
    else:
        # 面转栅格
        tif_name = tif_temp+os.sep+name+'.tif'
        arcpy.PolygonToRaster_conversion(shp_name, 'coast', tif_name, 'CELL_CENTER', 'NONE', cell)

        print('successful {}'.format(name))

        # 返回tif数据的路径
        return tif_name


def process(result_path):

    # 设置字段限制
    arcpy.env.qualifiedFieldNames = False

    # 森林公园,文件下的文件名
    forsets = glob.glob(data_forest + os.sep + '*.shp')
    dirs = os.listdir(path_data)
    for dir1, forset in zip(dirs, forsets):

        if dir1 == u'上饶物流园土地使用规划图':
            continue

        # 研究区
        study_areas = glob.glob(path_data+os.sep+dir1+os.sep+"*.shp")
        # study_areas = glob.glob(data_study_area+'*.shp')

        for study_area in study_areas:
            # 研究区的名字
            name = os.path.basename(study_area).split('.')[0]

            # 如果森林公园数据为空，就退出函数
            if arcpy.management.GetCount(forset)[0] == '0':
                print('fail to {}'.format(name))
                continue

            start_('data_handle')
            # # 处理高速
            # tif_name_freeway = fun(data_freeway, study_area, name+'freeway', 200, 5, 20)
            # # 如果没有重叠就跳出函数
            # if tif_name_freeway == -1:
            #     continue
            # # 处理河流
            # tif_name_river = fun(data_river, study_area, name+'river', 80, 5, 0, False)
            # # 如果没有重叠就跳出函数
            # if tif_name_river == -1:
            #     continue
            # # 处理铁路
            # tif_name_railway = fun(data_railway, study_area, name+'railway', 300, 5, 30)
            # # 如果没有重叠就跳出函数
            # if tif_name_railway == -1:
            #     continue
            # # 处理道路
            tif_name_road = fun(data_road, study_area, name+'road', 150, 5, 15)
            # 如果没有重叠就跳出函数
            if tif_name_road == -1:
                continue
            end_('data_handle')

            # 面转栅格
            tif_name = tif_temp+os.sep+name+'.tif'
            start_('PolygonToRaster_conversion')
            arcpy.PolygonToRaster_conversion(study_area, 'LNAME', tif_name, 'CELL_CENTER', 'NONE', 2)
            end_('PolygonToRaster_conversion')

            # 复制栅格：改变栅格像元深度
            start_('CopyRaster_management')
            tif_name_copy = tif_temp+os.sep+name+'copy.tif'
            arcpy.CopyRaster_management(tif_name, tif_name_copy, pixel_type='32_BIT_UNSIGNED')
            end_('CopyRaster_management')

            # 添加字段
            start_('AddField_management')
            arcpy.AddField_management(tif_name_copy, 'coast', 'FLOAT')
            end_('AddField_management')

            # # 计算字段
            # start_('CalculateField_management')
            # # excel路径
            # path = r"D:\ecology\class.xls"
            # df = pd.read_excel(path, header=1)
            # # 用于存放分类数据
            # table = []
            # # for i in range(6):
            # #     temp_arr = np.array(df.iloc[:, i:i+1])
            # #     temp_list = temp_arr.tolist()
            # #     table.append(temp_list)
            #
            # for i in range(6):
            #     table.append(np.array(df.iloc[:, i:i+1]).tolist())
            #
            # codeblock = '''
            # def fun(field):
            #     if field in "{}":
            #         return 5
            #     elif field in "{}":
            #         return 5
            #     elif field in "{}":
            #         return 50
            #     elif field in "{}":
            #         return 150
            #     elif field in "{}":
            #         return 10
            #     elif field in "{}":
            #         return 0
            # '''.format(",".join('%s' %id for id in table[0]), ",".join('%s' %id for id in table[1]),
            #            ",".join('%s' %id for id in table[2]), ",".join('%s' %id for id in table[3]),
            #            ",".join('%s' %id for id in table[4]), ",".join('%s' %id for id in table[5]))
            #
            # expression = 'fun(!LNAME!)'
            # arcpy.CalculateField_management(tif_name_copy, 'coast', expression, "PYTHON_9.3", codeblock)
            # end_('CalculateField_management')

            # 给新字段赋值
            start_('UpdateCursor')
            # excel路径
            path = r"D:\ecology\class.xls"
            df = pd.read_excel(path, header=None)
            # 用于存放分类数据
            table = []
            # for i in range(6):
            #     temp_arr = np.array(df.iloc[:, i:i+1])
            #     temp_list = temp_arr.tolist()
            #     table.append(temp_list)

            for i in range(6):
                table.append(df.iloc[:, i:i+1])

            # 不排序的求唯一值
            def np_unranked_unique(nparray):
                n_unique = len(np.unique(nparray))
                ranked_unique = pd.DataFrame(np.zeros([n_unique]))
                i = 0
                for x in nparray:
                    x = str(x)
                    # 中文匹配正则
                    chinese_pattern = '[\u4e00-\u9fa5]+'
                    # 将list转位str
                    x = re.findall(chinese_pattern, x)[1]
                    # 判断里面是否已经存在
                    if x not in ranked_unique.values:
                        ranked_unique.iloc[i:i+1, :] = x
                        i += 1
                return np.array(ranked_unique).tolist()

            # 获取研究区的LANAME字段值
            field = []
            with arcpy.da.SearchCursor(study_area, 'LNAME') as cursor:
                for row in cursor:
                    field.append(row)
                # 去除重复值
                field = np_unranked_unique((field))

            # 删除字段LNAME
            arcpy.DeleteField_management(tif_name_copy, 'LNAME')

            # 添加字段
            arcpy.AddField_management(tif_name_copy, 'LNAME', "TEXT", field_length=100)

            # 替换栅格中的LNAME
            with arcpy.da.UpdateCursor(tif_name_copy, ['LNAME']) as cursor:
                for i, row in enumerate(cursor):
                    # 将list转为str并转为中文
                    row[0] = (field[i])[0].encode('utf-8').decode('unicode_escape')
                    cursor.updateRow(row)
            del field

            # 通过LNAME进行分类
            with arcpy.da.UpdateCursor(tif_name_copy, ["LNAME", "coast"]) as cursor:
                for row in cursor:
                    if row[0] in table[0].values:
                        row[1] = 5
                    elif row[0] in table[1].values:
                        row[1] = 5
                    elif row[0] in table[2].values:
                        row[1] = 50
                    elif row[0] in table[3].values:
                        row[1] = 150
                    elif row[0] in table[4].values:
                        row[1] = 10
                    elif row[0] in table[5].values:
                        row[1] = 0
                    cursor.updateRow(row)
            end_('UpdateCursor')

            # 镶嵌至新栅格
            start_('MosaicToNewRaster_management')
            arcpy.MosaicToNewRaster_management('{};{};{};{};{}'.format(tif_name_copy, tif_name_road, tif_name_railway, tif_name_river, tif_name_freeway),
                                                tif_temp.split('/')[0], name+'new.tif', tif_name_copy, '8_BIT_UNSIGNED', 5, 1, 'MAXIMUM', 'FIRST')
            end_('MosaicToNewRaster_management')

            # 创建常量栅格
            start_('CreateConstantRaster')
            save_raster = r'D:\ecology\temp\tif'
            outConstRaster = CreateConstantRaster(150, 'INTEGER', 5, tif_name_copy)
            outConstRaster.save(save_raster+os.sep+name+'constant.tif')
            end_('CreateConstantRaster')

            # 镶嵌至新栅格
            start_('MosaicToNewRaster_management')
            arcpy.MosaicToNewRaster_management('{tif_};{}'.format())
            end_('MosaicToNewRaster_management')

            # 成本距离
            start_('CostDistance_sa')
            outCostDistance = arcpy.gp.CostDistance_sa(forset, tif_temp+os.sep+name+'new.tif', '', tif_temp+os.sep+name+'outbklink.tif')
            outCostDistance.save(tif_temp+os.sep+name+'outcostdist.tif')
            end_('CostDistance_sa')

            start_('CostPath')
            outCostPath = arcpy.gp.CostPath(forset, 'FID', tif_temp+os.sep+name+'outcostdist.tif', tif_temp+os.sep+name+'outbklink.tif', 'EACH_CELL')
            outCostPath.save(result_path+name+'.tif')
            end_('CostPath')

            print('sucessful {}'.format(name))

if __name__ == '__main__':
    result = r"D:\ecology\result"
    process(result)


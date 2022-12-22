# coding:utf-8
import arcpy
import glob
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\ecology\temp\shp"

# z盘数据
path_data = r"D:\python\ecology\data/"
path_data = unicode(path_data, 'utf-8')

# shp数据暂存
shp_temp = r"D:\python\ecology\temp\shp"
shp_temp = unicode(shp_temp, 'utf-8')

# 结果数据
result = r"D:\python\ecology\result"
result = unicode(result, 'utf-8')

table = []

# 文件下的文件名
dirs = os.listdir(path_data)
for dir1 in dirs:

    if dir1 == u'上饶物流园土地使用规划图':
        continue

    shps = glob.glob(path_data+dir1+os.sep+"*.shp")

    for shp in shps:

        name = os.path.basename(shp).split('.')[0]

        # 添加几何属性
        arcpy.AddGeometryAttributes_management(shp, 'AREA', '', 'SQUARE_METERS', '')

        # 创建矢量图层
        arcpy.MakeFeatureLayer_management(shp, "lyr")

        # 按属性选择
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "LNAME = '公园绿地'")

        outpath = shp_temp+os.sep+name+'.shp'
        arcpy.CopyFeatures_management("lyr", outpath)

        arcpy.Delete_management("lyr")

        # arcpy.FeatureToPoint_management(outpath, result+os.sep+name+'.shp', 'CENTROID')

def fun(path, outpath):
    table = []
    shps = glob.glob(path+os.sep+"*.shp")

    for shp in shps:

        name = os.path.basename(shp).split('.')[0]

        with arcpy.da.SearchCursor(shp, 'POLY_AREA') as cursor:
            for row in cursor:
                table.append(row[0])
            table.reverse()

        # 创建矢量图层
        arcpy.MakeFeatureLayer_management(shp, "lyr")

        if len(table) > 4:
            # 按属性选择
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "POLY_AREA >= {}".format(table[4]))

        # 复制图层要素
        arcpy.CopyFeatures_management("lyr", outpath+os.sep+name+'.shp')

        # 修复几何
        arcpy.RepairGeometry_management(outpath+os.sep+name+'.shp')

        # 删除图层数据
        arcpy.Delete_management("lyr")

        print('successful {}'.format(name))

if __name__ == '__main__':
    fun(shp_temp, result)
    print('all successful')
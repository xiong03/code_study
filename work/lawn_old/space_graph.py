# -*-*- coding: utf-8 -*
import arcpy
import os
import glob
import sys

# 编码转换
reload(sys)
sys.setdefaultencoding('utf-8')
arcpy.CheckOutExtension("Spatial")
# 如果文件已存在就覆盖
arcpy.env.overwriteOutput = True

# arcpy.env.workspace = r'C:\Users\xiong\Desktop\result\temp'

path = r'C:\Users\xiong\Desktop\result\tif'
outpath = r'D:\work\change\jpg'

for tif in glob.glob(path+os.sep+'*.tif'):

    name = os.path.basename(tif).split('.')[0]
    # 加载地图文档
    mxd = arcpy.mapping.MapDocument(r'D:\work\change\mxd\format.mxd')

    # # 调出“图层”数据框
    # layer = arcpy.mapping.ListDataFrames(mxd, '*')[0]
    # # 在数据框下的所有图层
    # lyrs = arcpy.mapping.ListLayers(mxd, "", layer)

    # 对栅格数据进行替换，矢量数据跳过
    for lyrs in arcpy.mapping.ListDataFrames(mxd, '*'):
        for lyr in lyrs:
            if not lyr.isFeatureLayer:
                # 修改数据源(工作空间路径，工作空间类型，数据集名称)
                lyr.replaceDataSource(path, "RASTER_WORKSPACE", name)
                # 返回布局中布局元素的 Python列表
                # ListLayoutElements (map_document[所引用的mxd],
                # {element_type}[一个字符串，表示将用于过滤返回的元素列表的元素类型。]
                # {wildcard}[限制结果])
                title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
                title.text = "青藏地区 %s 至 %s 草地变化" % (name.split("_")[0], name.split("_")[1])

    # 刷新地图和布局窗口
    arcpy.RefreshActiveView()
    # 刷新内容列表
    arcpy.RefreshTOC()
    # 输出
    outfile = outpath + os.sep + name + '.jpg'
    arcpy.mapping.ExportToJPEG(mxd, outfile, resolution=300)
    del mxd
    print("finish {}".format(name))



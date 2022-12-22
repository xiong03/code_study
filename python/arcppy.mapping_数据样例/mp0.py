# -*-*- coding: utf-8 -*
import arcpy
import os
from datetime import datetime
import sys

# 编码转换
reload(sys)
sys.setdefaultencoding('utf-8')

export_path = r"D:\arcppy.mapping_sjyl\out"
path = r"D:\arcppy.mapping_sjyl\土壤侵蚀"
path = unicode(path, 'utf-8')
arcpy.env.workspace = path  # 工作环境
names = []
tp = []

# 获取需要处理的栅格数据
# 获取需要处理的栅格数据 tip:这样获取的是字符串格式
file_list = os.listdir(path)
for fl in file_list:
    if os.path.splitext(fl)[0][-3:] == "prj" and os.path.splitext(fl)[1] == ".tif":
        names.append(fl)
for name in names:
    tif_path = r"D:\arcppy.mapping_sjyl\土壤侵蚀" + os.sep + name
    # 返回数据的属性，结果是地理处理结果对象。要获取字符串值，请使用结果对象的 getOutput 方法。
    # arcpy.GetRasterProperties_management (in_raster, {property_type}, {band_index})
    for tp_i in ["TOP", "BOTTOM", "LEFT", "RIGHT"]:
        tp_0 = [float(arcpy.GetRasterProperties_management(tif_path, tp_i).getOutput(0).encode("utf-8"))]
        tp = tp + tp_0
    a = tp[0]-tp[1]
    b = tp[3]-tp[2]
    if a > b:
        mapping_map = "mapping2.mxd"
    else:
        mapping_map = "mapping1.mxd"
    tp = []

    # 加载地图文档
    mxd_path = r'D:\arcppy.mapping_sjyl' + os.sep + mapping_map
    mxd = arcpy.mapping.MapDocument(mxd_path)

    # 调出“图层”数据框
    layer = arcpy.mapping.ListDataFrames(mxd, "图层")[0]

    # 在数据框下的所有图层
    lyrs = arcpy.mapping.ListLayers(mxd, "", layer)
    for lyr in lyrs:
        if lyr.isFeatureLayer:
            tle_0 = '"NAME" = \'%s\'' % (name.split(".")[0].split("_")[0])
            lyr.definitionQuery = tle_0  # 只显示需要的数据
        else:
            # 修改数据源(工作空间路径，工作空间类型，数据集名称)
            lyr.replaceDataSource(path, "RASTER_WORKSPACE", name.split(".")[0])
            # 返回布局中布局元素的 Python列表
            # ListLayoutElements (map_document[所引用的mxd],
            # {element_type}[一个字符串，表示将用于过滤返回的元素列表的元素类型。]
            # {wildcard}[限制结果])
            title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[1]
            title.text = "%s土壤侵蚀空间分布" % name.split("_")[0]
            # 更新布局视图范围
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            df.extent = lyr.getExtent()
            # 调整比例尺
            sc = arcpy.mapping.ListLayoutElements(mxd, "DATAFRAME_ELEMENT")[0]
            sc.scale = int(sc.scale * 0.0001) * 10000

    # 刷新地图和布局窗口
    arcpy.RefreshActiveView()
    # 刷新内容列表
    arcpy.RefreshTOC()
    # 输出
    export_path = r"D:\arcppy.mapping_sjyl\out" + os.sep + title.text
    arcpy.mapping.ExportToTIFF(mxd, export_path, resolution=300)
    del mxd
    print("finish")

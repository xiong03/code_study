# -*-*- coding: utf-8 -*
import arcpy
import arcpy.mapping as mapping
import os, re
arcpy.env.overwriteOutput = True#如果结果和文件夹中文件相同会覆盖
arcpy.CheckOutExtension("Spatial")

fdir = r'D:\python作业\arcppy.mapping_数据样例'
fdir = unicode(fdir, 'utf-8')
fmxd1 = fdir + os.sep + 'test.mxd'
# fmxd2 = r'D:\arcpy\mapping\mxd\leanxian.mxd'

dir_rasters = r'D:\python作业\arcppy.mapping_数据样例\土壤侵蚀'
dir_rasters = unicode(dir_rasters, 'utf-8')
arcpy.env.workspace = dir_rasters
f_rasters = arcpy.ListRasters('*prj*', 'TIF')
# outpath = r'D:\arcpy\mapping\arcppy.mappingshuju\out'
# for i in replace_county:
# name = os.path.basename(i)
# title = os.path.splitext(name)[0]#去除文件名后缀  os.path.splitext(os.path.basename("hemanth.txt"))[0]
# desc = arcpy.Describe(i)
# data_extent = [desc.extent.XMin, desc.extent.XMax, desc.extent.YMin, desc.extent.YMax]#获取边界信息
# if (data_extent[1] - data_extent[0]) > (data_extent[3] - data_extent[2]):
#     fmxd =fmxd1
# else:
#     fmxd =fmxd2
# --------------------------------------------------------------
for f_raster in f_rasters:
    fn = os.path.basename(f_raster).split('_')[0]
    str0 = u".*土壤侵蚀$"
    str1 = u".*市.*区$"
    if re.search(str0, fn):
        fn = fn[:-4]
    if re.search(str1, fn):
        fn = fn.split(u'市')[1]
    print(fn)
# ---------------definitionQuery setting and replace data source------------
    strs = '"NAME" = \'%s\'' % (fn)
    desc = arcpy.Describe(f_raster)
    data_extent = [desc.extent.XMin, desc.extent.XMax, desc.extent.YMin, desc.extent.YMax]  # 获取边界信息
    mxd_sv = fdir + os.sep + fn + ".mxd"
    mxd = mapping.MapDocument(fmxd1)  # 读取mxd
    # mxd_scale = mapping.ListLayoutElements(mxd, "DATAFRAME_ELEMENT")[0].scale  # get layoutElement scale
    df = mapping.ListDataFrames(mxd)[0]  # 读取第一个数据框
    layers = mapping.ListLayers(mxd, "", df)
    for ly in layers:
        if ly.isFeatureLayer:
            ly.definitionQuery = strs
        else:
            ly.replaceDataSource(dir_rasters, "RASTER_WORKSPACE", f_raster) #替换数据源，i新数据源，name输出名称
            ly_extend = ly.getExtent() # 缩放至图层
            df.extent = ly_extend
            df.scale = int(df.scale * 0.0001) * 10000
   # -----------     TextElement setting---------------------
    tl = '\n'.join(list(fn))
    # titl = [fs + '\n' for fs in fn]
    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.text[-1] == u'布':
            TlName = elm.text.split(u'土')[1]
            elm.text = tl + '\n' + u'土' + TlName
            break
    arcpy.RefreshActiveView()  # 刷新地图和布局窗口
    arcpy.RefreshTOC()  # 刷新内容列表
    TifName = fdir + os.sep + fn + '.tif'
    mapping.ExportToTIFF(mxd, TifName, resolution=600)  # 输出为png,分辨率为300
    del mxd

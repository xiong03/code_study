# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 14:50:32 2022

@author: xiong
"""

from tqdm import tqdm
import os, glob
import rasterio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
# from matplotlib.pyplot import savefig
# from matplotlib.ticker import FuncFormatter
# import xml.etree.ElementTree as ET

def handle_color(color_path):
    colors = []

    with open(color_txt, encoding='utf-8') as file_obj:
        lines = file_obj.readlines()

    for line in lines:
        points = line.split(' ')
        colors.append([int(points[0]),int(points[1]),int(points[2]),int(points[3])])
        
    return colors

def classify(tif,windows,colors):
    print('cope raster...')
    result = pd.DataFrame([i[0] for i in colors],columns = ['X'])
    df = np.array([0]*len(colors))
    
    for win in tqdm(windows):
        temp = []
        with rasterio.open(tif) as scr:
            arr = scr.read(1,window=win)
            scr.close()
        del scr
        
        for value in result.values:
            temp.append(np.sum(arr == value[0]))
        
        df += np.array(temp)
    
    result['classify'] = pd.DataFrame(df/df.sum(axis=0))*100
    return result
    
# def plt_bar(result,axis):
#     fig, ax = plt.subplots()
#     fig = plt.figure(figsize=(15, 10))
    
#     if axis==0:
#         ax.bar(result['X'], result['classify'],
#                        width=MyPlt.width_bar,
#                        color=MyPlt.color_bar,
#                        # ls = MyPlt.linestyle,
#                        # ec = MyPlt.ed_color, # edgecolor
#                        lw=MyPlt.linewidth)
#         ax.set_xticks([])
#         frames = ['top', 'right', 'bottom']
#         direction = 'in'
#     else:
#         ax.barh(result['X'], result['classify'],
#                        width=MyPlt.width_bar,
#                        color=MyPlt.color_bar,
#                        # ls = MyPlt.linestyle,
#                        # ec = MyPlt.ed_color, # edgecolor
#                        lw=MyPlt.linewidth)
#         ax.set_yticks([])
#         ax.spines['bottom'].set_position(('axes', 1))
#         frames = ['right', 'bottom', 'left']
#         direction = 'out'
    
#     ax.tick_params(axis='both',
#                    direction=direction,
#                    labelsize=MyPlt.tick_labelsz)
    
#     for frame in frames:
#         ax.spines[frame].set_visible(False)
#     ax.locator_params(nbins=4)
    
#     return fig

def plot_bar(result,outfile):
    
    name = os.path.basename(outfile).split('.')[0]
    
    fig = plt.figure(figsize=(15, 10))
    plt.rcParams['font.sans-serif']=['SimSun'] #用来正常显示中文标签
    plt.xlabel('value',fontsize=30)
    plt.ylabel('precentage(100%)',fontsize=30)
    plt.xlim(10,80) #设置x轴范围
    plt.suptitle(f'{name}西藏地区草地类型转化空间分布',fontsize=45) #添加标题
    
    # 设置x轴刻度
    ax=plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(5))

    #数据可视化
    plt.bar(result['X'],result['classify'],color=MyPlt.color_bar)
    
    plt.savefig(outfile,dpi=500)
    print(f'successful {outfile}')

if __name__ == '__main__':
    
    path = r'D:\0\text\result2'
    outpath = r'D:\0\text\jpg2'
    color_txt = r'D:\0\text\2015-2010.tif.clr'
    colors = handle_color(color_txt)
    color_lst = [[i[1],i[2],i[3]] for i in colors]
    
    class MyPlt:
        font_prop = 'Times New Roman'
        linestyle = ''
        linewidth = 0
        font_xlabel = ''
        font_ylabel = ''
        font_porp = ''
        fontsz = 12
        tick_labelsz = 12
        color_bar = list(map(lambda x: x / 255, np.array(color_lst)))
        facecolor = ''
        ax_facecolor = ''
        ed_color = 'None'
        width_bar = 0.3
        width_spines = ''
        dpi = 600
    
    tifs = glob.glob(path+os.sep+'*.tif')
    with rasterio.open(tifs[0]) as scr:
        windows = [window for ij, window in scr.block_windows()]
        scr.close()
    del scr
    
    for tif in tifs:
        name = os.path.basename(tif).split('.')[0]
        outfile = outpath+os.sep+f'{name}.jpg'
        result = classify(tif,windows,colors)
        
        plot_bar(result,outfile)
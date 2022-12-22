# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 15:11:27 2022

@author: xiong
"""

import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

landuse1 = {'11':'水田','12':'旱地','21':'有林地','22':'灌木林','23':'疏木林','24':'其他林地',
           '31':'高覆盖草地','32':'中覆盖草地','33':'低覆盖草地','41':'河渠','42':'湖泊',
           '43':'水库抗康','44':'永久性冰川雪地','45':'滩涂','46':'滩地','51':'城镇用地',
           '52':'农村居民地','53':'其他建筑用地','61':'沙地','62':'戈壁','63':'盐碱地',
           '64':'沼泽地','65':'裸土地','66':'裸岩石质地','67':'其他','255':'未分类',}

landuse2 = {'1':'温性草甸草原类','2':'温性草原类','3':'温性荒漠草原类','4':'高寒草甸草原类',
            '5':'高寒草原类','6':'高寒荒漠草原类','7':'温性草原化荒漠类','8':'温性荒漠类',
            '9':'高寒荒漠类 ','10':'热性草丛类','11':'热性灌草丛类','12':'暖性草丛类',
            '13':'暖性灌草丛类','14':'低地草甸类','15':'温性山地草甸类','16':'高寒草甸类',
            '17':'沼泽类','0':'未分类'}

# 数字转文字
def funcation(Value):
    str1 = str(int(Value//100))
    str2 = str(int(Value%100))
    
    name1 = landuse1[str1]
    name2 = landuse2[str2]
        
    # if name1 == name2:
    #     return np.nan
    # else:
    return name1+'->'+name2


# 出图
def plot_bar(x,y,outfile):
    plt.figure(figsize=(15, 30))
    plt.rcParams['font.sans-serif']=['SimSun'] #用来正常显示中文标签
    plt.xlabel('percentage',fontsize=17,)
    plt.ylabel('种类',fontsize=17)
    plt.xlim(0,int(round(max(y),0))+1)
    plt.suptitle(os.path.basename(outfile).split('.')[0],
                 x=0.1, y=0.95, fontsize=30, color='red')
    
    plt.barh(x,y,color=colors)
    
    
    # ax=plt.gca()
    # #ax为两条坐标轴的实例
    # ax.yaxis.set_major_locator(MultipleLocator(1))
    # #把x轴的主刻度设置为1的倍数

    
    # ax1 = fig.add_subplot(1,1,1)
    # ax1.barh(x, y)
    # plt.xticks([]) #设置x的刻度和标签
    # plt.yticks([]) #设置y的刻度和标签
    # ax1.tick_params()
    # ax1.set_facecolor() #设置绘图背景颜色
    # ax1.spines['top'].set_visible(False) #去掉上边框
    # ax1.spines['right'].set_visible(False) #去掉右边框
    # ax1.spines['left'].set_linewidth(lw_spines) #设置左坐标轴宽度
    # ax1.spines['bottom'].set_linewidth(lw_spines) #设置底部坐标轴宽度
    # ax1.spines['right'].set_linewidth(lw_spines) #设置左坐标轴宽度
    # ax1.spines['top'].set_linewidth(lw_spines) #设置顶部坐标轴宽度
    # ax1.yaxis.set_ticks_position('none')
    # ax1.xaxis.set_ticks_position('none')
    # plt.show()
    plt.savefig(outfile,dpi=500)
    print(f'successful {outfile}')


# 柱状图颜色
color_lst = [[0,92,230],[0,112,225],[115,178,225],[190,210,225],[225,225,225],
             [204,204,204],[178,178,178],[156,156,156],[255,235,175],[255,211,127],
             [255,170,0],[230,152,0],[255,0,0],[168,0,0],[115,0,0]]
colors = list(map(lambda x: x / 255, np.array(color_lst)))

path = r'C:\Users\xiong\Desktop\result\excel'
outpath = r'C:\Users\xiong\Desktop\result\jpg'

for file in glob.glob(path+os.sep+'*.xls'):
    
    outfile = outpath+os.sep+os.path.basename(file).split('.')[0]+'.jpg'
    if '30' not in file:
        continue
    df = pd.read_excel(file)
    
    # 将像元数小于30的去掉，将无变化去掉
    df.where(df['Count']>=30, inplace=True)
    df.where(df['Value']//100 != df['Value']%100, inplace=True)
    df = df[df['Value'].notna()]
    df.reset_index(inplace=True,drop=True)
    
    # 添加种类占比
    df['percentage'] = pd.DataFrame(df['Count']/df['Count'].sum(axis=0))

    # 获取柱状图的xy值
    X = df['Value'].map(funcation).tolist()
    Y = (df['percentage']*100).tolist()
    
    plot_bar(X,Y,outfile)


# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 20:16:33 2022

@author: xiong
"""

import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

landuse = {'11':'水田','12':'旱地','21':'有林地','22':'灌木林','23':'疏木林','24':'其他林地',
           '31':'高覆盖草地','32':'中覆盖草地','33':'低覆盖草地','41':'河渠','42':'湖泊',
           '43':'水库抗康','44':'永久性冰川雪地','45':'滩涂','46':'滩地','51':'城镇用地',
           '52':'农村居民地','53':'其他建筑用地','61':'沙地','62':'戈壁','63':'盐碱地',
           '64':'沼泽地','65':'裸土地','66':'裸岩石质地','67':'其他','255':'未分类'}

landuse1 = {'1':'耕地','2':'林地','3':'草地','4':'水域','5':'建筑用地','6':'未利用地'}


# # 数字转文字
# def funcation(Value):
#     str1 = str(int(Value//100))
#     str2 = str(int(Value%100))
    
#     name1 = landuse[str1]
#     name2 = landuse[str2]
        
#     # if name1 == name2:
#     #     return np.nan
#     # else:
#     return name1+'->'+name2

# 用判断数据是否需要合并，name1|2为str1|2
def handle(Value,name1,name2):
    
    # 用于存储结果
    x,y = [[],[]]
    
    # 先筛选name1
    for i in range(1,7):
        if i == 3:
            continue
        filter_data = Value[Value[name1].str.startswith(str(i))]
        # 再筛选name2
        for j in range(31,34):
            data = filter_data[filter_data[name2].str.contains(str(j))]
            # 判断改组占比是否大于0.5
            if data['percentage'].sum() < 0.5:
                # 安装name1不同来判断名字
                if name1 == 'str1':
                    x.append(landuse1[str(i)]+'->'+landuse[str(j)])
                    y.append(data['percentage'].sum()*100)
                else:
                    x.append(landuse[str(j)]+'->'+landuse1[str(i)])
                    y.append(data['percentage'].sum()*100)
                    
    return x,y
                
            
# 将占比大的数据进行细分，占比小的数据进
def group(Value):
    Value['str1'] = Value['Value']//100
    Value['str2'] = Value['Value']%100
    Value['str1'] = Value['str1'].astype('str')
    Value['str2'] = Value['str2'].astype('str')
    
    # 先计算前到后
    x1,y1 = handle(Value,'str1','str2')
    # 后计算后到前
    x2,y2 = handle(Value,'str2','str1')
    
    x1.extend(x2)
    y1.extend(y2)
    
    return x1, y1

# 出图
def plot_bar(x,y,outfile):
    fig = plt.figure(figsize=(15, 10))
    plt.rcParams['font.sans-serif']=['SimSun'] #用来正常显示中文标签
    plt.xlabel('percentage',fontsize=17)
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
    
    if '30' in file:
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
    X,Y = group(df[['Value','percentage']])
    
    plot_bar(X,Y,outfile)
    
    
    
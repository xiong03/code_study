# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:56:11 2022

@author: xiong
"""

import pandas as pd
import glob, os
import numpy as np
import matplotlib.pyplot as plt

path = r'D:\work\new\txt\result'
names = ['NDVI','EVI']
colors = ['y','blue','coral','green','c','red','m','k']
titles = ['高寒草甸类1','高寒草原类2','山地草甸类3','温性草原类4','低地草甸类5','温性荒漠类6','高寒荒漠类7']
j=0

for file in glob.glob(path+os.sep+'*.csv'):
    outfile = path+os.sep+os.path.basename(file).split('.')[0]+'.png'
    a = pd.DataFrame()
    
    # if os.path.exists(outfile):
    #      continue

    # if not int(os.path.basename(file).split('.')[0])==7:
    #     continue

    df = pd.read_csv(file)
    data = df.iloc[:,1:1+2].T
    
    a['max'] = data.quantile(0.75,axis=1)
    a['min'] = data.quantile(0.25,axis=1)
    
    for i in range(a.shape[0]):
        xmax = float(a['max'][i:i+1])
        xmin = float(a['min'][i:i+1])
        
        c = data[i:i+1]
        c.where((c<=xmax)&(c>=xmin),inplace=True)
        data[i:i+1] = c
        
    a['mean'] = data.mean(axis=1)
    a['max'] = data.max(axis=1)
    a['min'] = data.min(axis=1)
    result = pd.DataFrame()
    
    for i in range(0,13):
        b = a.reset_index()
        b['name'] = b['index']+f'_{i}'
        b.set_index(['name'],inplace=True,drop=True)
        del b['index']
        result = pd.concat([result,b],axis=0)
    
    result.reset_index(inplace=True)
    result = pd.concat([result,result['name'].str.split('_', expand=True)],axis=1)
    
    elevation = result[result[0].str.contains('slope')].copy()
    # EVI = a[a[0].str.contains('EVI')]

    plt.style.use('ggplot')
    # font = FontProperties(fname="SimHei.ttf", size=14)
    plt.figure(num=3,figsize=(15,8))
    plt.xlabel('month')
    plt.ylabel('指数',fontdict={"family": "KaiTi", "size": 15, "color": "black"})
    plt.title('slope')
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
        
    plt.plot(elevation[1],elevation['mean'],color=colors[j],label=titles[j])
    # plt.plot(NDVI[1],NDVI['min'],'-.',color=colors[j])
    # plt.plot(NDVI[1],NDVI['max'],'--',color=colors[j])
    plt.fill_between(elevation[1], elevation['max'], y2=elevation['min'], color=colors[j], alpha = 0.2)
    
    plt.legend(loc=0,ncol=1,shadow=True)
    j+=1
plt.savefig(outfile,dpi = 500)
plt.show()
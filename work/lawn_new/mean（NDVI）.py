# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:05:57 2022

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
    data = df.iloc[:,3:3+24].T
    data.where((data<1)&(data>0),inplace=True)
    
    # a['mean'] = data.mean(axis=1)
    # a['var'] = data.var(axis=1)
    
    # a['max'] = a['mean']+(1.96*a['var'])/math.sqrt(df.shape[0])
    # a['min'] = a['mean']-(1.96*a['var'])/math.sqrt(df.shape[0])
    
    # a['max'] = data.mean(axis=1)+data.std(axis=1)*2
    # a['min'] = data.mean(axis=1)-data.std(axis=1)*2
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
    a.reset_index(inplace=True)
    a = pd.concat([a,a['index'].str.split('_', expand=True)],axis=1)
    
    NDVI = a[a[0].str.contains('EVI')].copy()
    # EVI = a[a[0].str.contains('EVI')]

    plt.style.use('ggplot')
    # font = FontProperties(fname="SimHei.ttf", size=14)
    plt.figure(num=3,figsize=(15,8))
    plt.xlabel('month')
    plt.ylabel('指数',fontdict={"family": "KaiTi", "size": 15, "color": "black"})
    plt.title('EVI')
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.plot(NDVI[1],NDVI['mean'],color=colors[j],label=titles[j])
    # plt.plot(NDVI[1],NDVI['min'],'-.',color=colors[j])
    # plt.plot(NDVI[1],NDVI['max'],'--',color=colors[j])
    plt.fill_between(NDVI[1], NDVI['max'], y2=NDVI['min'], color=colors[j], alpha = 0.2)
    
    plt.legend(loc=0,ncol=1,shadow=True)
    
    j+=1
plt.savefig(outfile,dpi = 500)
plt.show()
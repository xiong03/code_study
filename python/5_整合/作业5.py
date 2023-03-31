# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 16:16:17 2022

@author: xiong
"""

import os
import pandas as pd
import glob

def zhenghe(str1):
    path = r'D:\python\5_整合'
    dirs = os.listdir(path)
    #按照元素大小进行排序
    dirs = sorted(dirs, key=lambda x:len(x))
    df = pd.DataFrame()
    for dir in dirs:
        if "." in dir:
            continue
        txt = path+os.sep+dir+os.sep+str1+" "+dir+".txt"
        df1 = pd.read_csv(txt,encoding = 'gb2312')
        if "站名" not in df.columns:
            df = df1[["站名","站号","经度","纬度"]]
        data = df1.iloc[:,4:5]
        df.insert(loc=len(df.columns), column=dir, value=data)
    outpath = path+os.sep+str1+".txt"
    df.to_csv(outpath,index=False,header=True)

str0 = ["Maxi T","Mini T","P","RH","S","WS"]
for str1 in str0:
    zhenghe(str1)
    print("successful {}".format(str1))
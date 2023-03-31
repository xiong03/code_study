# -*- coding: utf-8 -*-
"""
Created on Thu May 19 20:51:37 2022

@author: xiong
"""

import time
from multiprocessing import Pool
import multiprocessing
import numpy as np
import pandas as pd
import glob,os

#读取数据并整理
def fun(str0:str):
    path = r"D:\python\6 数据分组\files"
    str2 = "2018\8\Maxi T 1-15.txt"
    result = []
    for year in range(2015,2021):
        data1 = pd.DataFrame()
        for str1 in str0:
            data = pd.DataFrame(columns=[str1])
            for month in range(1,13):
                txts = glob.glob(path+os.sep+str(year)+os.sep+str(month)+os.sep+str1+"*.txt")
                for txt in txts:
                    df = pd.read_csv(txt, encoding='gb2312', sep=",")
                    if str2 in txt:
                        df1 = np.full((88, 1), np.nan)
                        df1 = pd.DataFrame(df1)
                    else:
                        df1 = df.iloc[:,4:5]
                    df1.columns = [str1]
                    data = pd.concat([data,df1])
            data1.insert(loc=len(data1.columns), column=str1, value=data)
        data1 = data1.T
        data_result = np.array(data1)
        result.append(data_result)
    return result


#数据分组
def fun1(data):
    path = r"D:\python\6 数据分组\files\2015\1\Maxi T 1-15.txt"
    df1 = pd.read_csv(path, encoding='gb2312', sep=",")
    df = df1.iloc[:,:4]
    data1 = data.reshape(24,88).T
    data1 = pd.DataFrame(data1)
    df = pd.concat([df,data1],axis=1)
    return df

start = time.time()
str0 = ["Maxi T","Mini T","P","RH","S","WS"]
years = range(2015,2021)
result = fun(str0)
outpath = r"D:\python\6 数据分组\result"
if __name__ == "__main__":
    for data,year in zip(result,years):
        cores = multiprocessing.cpu_count()
        pool = Pool(cores)
        df = pool.map(fun1, data)
        for i,str1 in zip(range(6),str0):
            data_result = df[i]
            data_result.to_csv(outpath+os.sep+str1+str(year)+".txt")
            print('successful {} {}'.format(year,str1))
        print('successful {}'.format(year))
    print("all successful")
end = time.time()
print(end-start)         

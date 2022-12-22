# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:35:19 2022

@author: xiong
"""

import pypyodbc
import pandas as pd
import numpy as np
from multiprocessing import Pool
import multiprocessing
import traceback

def select_all(sql, args=None):
     """查询表中数据"""
     #链接数据库
     MDB = r'D:\python\mdb文件\MeteoData20192020.mdb'  # 文件路径
     DRV = '{Microsoft Access Driver (*.mdb,*.accdb)}'   # 链接的数据库
     try:
         con = pypyodbc.win_connect_mdb(f'Driver={DRV};DBQ={MDB};')
     except:
         print("数据库连接失败！请检查！")
     results = pd.read_sql(sql,con)
     return results

def get_data(year,names):
    sql = r"SELECT * FROM " + "all{}".format(str(year))
    df  = select_all(sql)
    df1 = df[names]
    df1["date"] = (df["月"]*100+df["日"]).copy()
    df1.drop_duplicates(subset=["台站","date"],inplace=True,keep='first')
    return df1

def calculate(name, data):
    data = np.array(data)
    df2 = pd.DataFrame(data.reshape(int(data.shape[0]/366),366))
    result = pd.DataFrame()
    for i in range(1,47):
        df = df2.iloc[:,8*(i-1):8*i]
        if name == "降水量":
            result[i] = df.sum(1)
        else:
            result[i] = df.mean(1)
        # result[i] = df.sum(1)
    return result

names = ["台站","日最高气温","日最低气温","日照时数","平均风速","平均相对湿度","降水量"]
data = []

if __name__ == '__main__':
    for year in range(2019,2021):
        df = np.array(get_data(year, names)[names[1:]]).T
        for i in df:
            data.append(pd.DataFrame(i))
        cores = multiprocessing.cpu_count()
        pool = Pool(cores)
        parameter = list(zip(names[1:],data))
        try:
            data1 = pool.starmap(calculate, parameter)
        except:
            traceback.print_exc()
        
        
        
        
        
        
        
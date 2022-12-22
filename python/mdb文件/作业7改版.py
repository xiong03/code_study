# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:16:05 2022

@author: xiong
"""

import pypyodbc
import pandas as pd
import os

def select_all(sql, args=None):
     """查询表中数据"""
     #链接数据库
     MDB = r'D:\python\mdb文件\MeteoData20192020.mdb'  # 文件路径
     DRV = '{Microsoft Access Driver (*.mdb,*.accdb)}'   # 链接的数据库
     try:
         con = pypyodbc.win_connect_mdb(f'Driver={DRV};DBQ={MDB};')
     except:
         print("数据库连接失败！请检查！")
         return 0, False
     results = pd.read_sql(sql,con)
     return results, True

def get_data(year,name):
    sql = r"SELECT * FROM " + "all{}".format(str(year))
    df,df_bool  = select_all(sql)
    if not df_bool:
        return 0,False
    df1 = df[["台站",name]]
    df1["date"] = df["月"]*100+df["日"]
    df1.drop_duplicates(subset=["台站","date"],inplace=True,keep='first')
    df1.set_index(["台站","date"],inplace=True)
    df2 = df1.unstack()
    df2.columns = list(range(1,df2.shape[1]+1))
    return df2,True

def calculate(year,name):
    result = pd.DataFrame()
    df2,df2_bool = get_data(year,name)
    if not df2_bool:
        return 0,False
    for i in range(1,47):
        data = df2.iloc[:,8*(i-1):8*i]
        if name == "降水量":
            result[i] = data.sum(1)
        else:
            result[i] = data.mean(1)
    return result,True
  

names = ["日最高气温","日最低气温","日照时数","平均风速","平均相对湿度","降水量"]

for year in range(2019,2021):
    for name in names:
        result,result_bool = calculate(year,name)
        if not result_bool:
            break
        print("successful {}".format(name))
        dirs = r"D:\python作业\mdb文件\{}".format(name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        outpath = dirs+os.sep+name+str(year)+".txt"
        result.to_csv(outpath,index=True,header=True,float_format='%.1f')
print("all suceessful")    
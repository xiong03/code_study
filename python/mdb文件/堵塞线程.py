# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:50:06 2022

@author: xiong
"""

import pypyodbc
import pandas as pd
import os
from queue import Queue
from threading import Thread
import traceback
import numpy as np

running = False

# 读取数据
class read:
    def __init__(self,queue):
        self.queue = queue
        
    def func(self,sql):

        MDB = r'D:\python\mdb文件\MeteoData20192020.mdb'  # 文件路径
        DRV = '{Microsoft Access Driver (*.mdb,*.accdb)}'   # 链接的数据库
        try:
            con = pypyodbc.win_connect_mdb(f'Driver={DRV};DBQ={MDB};')
        except:
            print("数据库连接失败！请检查！")
        results = pd.read_sql(sql,con)
        self.queue.put(results)


class handle(Thread):
    def __init__(self,queue,names,year):
        super().__init__()
        self.queue = queue
        self.names = names
        self.year = year
        
    def run(self):
        while running:
            data = self.queue.get()
            data.to_csv(self.year,index=True,header=True,float_format='%.1f')
            # for name in self.names[1:]:
            #     outfile = outpath+os.sep+f'{self.year}-{name}.csv'
            #     if os.path.exists(outfile):
            #         break
                
            #     df = data[names]
            #     df["date"] = (data["月"]*100+data["日"]).copy()
            #     df.drop_duplicates(subset=["台站","date"],inplace=True,keep='first')
                
            #     df1 = pd.DataFrame(np.array(df).reshape(int(data.shape[0]/366),366))
                
            #     result = pd.DataFrame()
                
            #     for i in range(1,47):
            #         df2 = df1.iloc[:,8*(i-1):8*i]
            #         if name == "降水量":
            #             result[i] = df2.sum(1)
            #         else:
            #             result[i] = df2.mean(1)
            #         # result[i] = df.sum(1)
                
            #     data.to_csv(outfile,index=True,header=True,float_format='%.1f')
            #     print(outfile)
                

if __name__ == '__main__':
    
    running = True
    
    queue = Queue()
    names = ["台站","日最高气温","日最低气温","日照时数","平均风速","平均相对湿度","降水量"]
    outpath = r'D:\python\mdb文件\result'
    
    reader = read(queue)
    
    threads = []
    
    for year in range(2019,2021):
        # for name in names:
        
        sql = r"SELECT * FROM " + f"all{year}"
        reader.func(sql)
        
        worker = handle(queue,names,year)
        threads.append(worker)
        try: 
            worker.start()
        except:
            traceback.print_exc()

    for i in threads:
        worker.join()
    running = False
            
            
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 20:28:19 2022

@author: xiong
"""

import pandas as pd
import numpy as np
from multiprocessing import Pool
import multiprocessing
import glob,os
import time

start = time.time()
def fun(str1):
    data_uni = pd.DataFrame()
    for year in range(2015,2021):
        outpath = os.path.join(path,str(year))
        for mon in range(1,13):
            files = path+os.sep+str(year)+os.sep+str(mon)
            txts = glob.glob(files+os.sep+"*.txt")
            for txt in txts:
                if str1 in txt:
                    str0 = "数据分组\\2018\8\Maxi T 1-15.txt"
                    if str0 in txt:
                        continue
                    data_txt = pd.read_table(txt, encoding='gb2312', sep=",")
                    if "1a" not in data_uni.columns:
                        data_uni = data_txt.iloc[:,:4]
                    data1 = data_txt.iloc[:,4:5]
                    if "1-15" in txt:
                        data_uni.insert(loc=len(data_uni.columns), column=str(mon)+"a", value=data1)
                    elif "16" in txt:
                        data_uni.insert(loc=len(data_uni.columns), column=str(mon)+"b", value=data1)
                        break
        data_uni.to_csv(outpath+os.sep+str1+str(year)+".txt",sep="\t",index=True,header=True)
        print("succeful {}".format(str1+str(year)))
        data_uni = pd.DataFrame()

path = r"D:\python\6 数据分组"
str0 = np.array(["Maxi T","Mini T","P","RH","S","WS"])
# cores = multiprocessing.cpu_count()
# pool = Pool(cores)
# pool.map(fun, str0)

for str1 in str0:
    fun(str1)
    
end = time.time()
print("time:{}".format(end-start))
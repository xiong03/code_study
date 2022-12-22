# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:18:52 2022

@author: xiong
"""

import pandas as pd
import glob, os

outpath = r'D:\work\new\txt\result'
path = r'D:\work\new\txt'

for name in range(1,8):
    outfile = outpath+os.sep+f'{name}.csv'
    
    if os.path.exists(outfile):
        continue
    files = glob.glob(path+os.sep+'*'+os.sep+f'{name}.csv')
    
    result = pd.read_csv(files[0])
    result.set_index(['CID'],drop=True,inplace=True)
    
    for file in files[1:]:
        df = pd.read_csv(file)
        df.set_index(['CID'],drop=True,inplace=True)
        
        result = pd.concat([result,df],axis=1)
    
    
    result.to_csv(outfile)
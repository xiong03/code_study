# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 17:12:23 2022

@author: xiong
"""

# 1-(10,7225), (-16,27) 351288
# 2-(1,4900), (-26,27) 519294
    
# import seaborn as sns
import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap
# from matplotlib.pyplot import MultipleLocator

file = r'D:\work\change\date_result\data_1\result.xlsx'
a = [i for i in range(10,7225,1)]
b = [i for i in range(-16,27,1)]
b.extend([i+0.5 for i in b])
b.sort()

df = pd.read_excel(file)
df.columns = ['raster_quantity']
df['precipitation [mm]'] = [i for i in a]*len(b)
df['temperature [°C]'] = [i for i in b]*len(a)
df = df[df['raster_quantity']>0]

outfile = r'D:\work\change\date_result\data_1\data.xlsx'

df.to_excel(outfile,index=None)


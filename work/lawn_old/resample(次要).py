# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 22:02:53 2022

@author: xiong
"""

import rasterio
import numpy as np
from rasterio.enums import Resampling
import glob, os
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator

# def save(temperature,percipation,grass,outfile):
#     # 设置xytable
#     plt.ylabel('percipation [mm]',fontsize=14)
#     plt.xlabel('temperature [°C]',fontsize=14)
    
#     # 设置xy范围
#     plt.ylim(0,50000)
#     plt.xlim(-20,30)
    
#     # 设置xy刻度
#     ax=plt.gca()
#     ax.xaxis.set_major_locator(MultipleLocator(10))
#     ax.yaxis.set_major_locator(MultipleLocator(10000))
    
#     # 设置颜色
#     cm = plt.cm.get_cmap('RdYlGn')
#     plt.scatter(temperature.reshape(-1),percipation.reshape(-1),
#                 c=grass.reshape(-1),marker='s',cmap=cm)
    
#     plt.colorbar()
#     plt.savefig(outfile,dpi=300)
#     plt.show()
    

def read(file, outfile):
    with rasterio.open(file) as scr:
        result = scr.read(out_shape=(1, outmeta['height'], outmeta['width']),
                          resampling=Resampling.bilinear).astype('float16')
        scr.close()
    del scr
    return result[0]

if __name__ == '__main__':
    path = r'D:\work\change\per_tem'
    files = glob.glob(path+os.sep+'*.tif')
    outpath = r'D:\work'
    
    # grass
    with rasterio.open(r'D:\work\草地资源图\clip.tif') as scr:
        grass = scr.read(1).astype('float16')
        outmeta = scr.meta.copy()
        scr.close()
        # outmeta.update({'dtype':'float32'})
        grass[(grass>=18)|(grass<=0)] = np.nan
    del scr
    
    outfile = outpath+os.sep+'result.png'
    
    percipation, temperature = [(read(files[0],outmeta)*1000).astype('int16'),
                                read(files[1],outmeta)]
    
    # 设置xytable
    plt.ylabel('percipation [mm]',fontsize=14)
    plt.xlabel('temperature [°C]',fontsize=14)
    
    # 设置xy范围
    plt.ylim(0,35000)
    plt.xlim(-20,25)
    
    # 设置xy刻度
    ax=plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5000))
    
    # 设置颜色
    cm = plt.cm.get_cmap('tab20b')
    plt.scatter(temperature.reshape(-1),percipation.reshape(-1),
                c=grass.reshape(-1),marker='s',cmap=cm)
    
    plt.colorbar()
    plt.savefig(outfile,dpi=300)
    plt.show()
    
    
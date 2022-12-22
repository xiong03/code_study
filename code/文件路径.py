# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 22:43:01 2022

@author: xiong
"""

def fun(path,formats,result):
    # path为根目录，为字符串。
    # formats为所需要获取的文件后缀名，为list，list里面为字符串形式。
    # result为结果文件路径，返回result
    import os,glob
    
    dirs1 = glob.glob(path+os.sep+'*')
    if len(dirs1) != 0:
        for format1 in formats:
            for dir1 in dirs1:
                if '.'+format1 in dir1:
                    files = glob.glob(path+os.sep+'*.'+format1)
                    result.extend(files)
        fun(path+os.sep+'*',formats,result)
    else:
        return
    
result = []
fun(r"D:\python",['py'],result)
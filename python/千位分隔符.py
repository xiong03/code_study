# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:36:32 2022

@author: xiong
"""

#1. 拆分成整数部分和小数部分
# 将数字转为字符串

number = 12345.45
number_str = str(number)
    
# 拆分成整数部分和小数部分

number_str_list = number_str.split('.')
integer_part = number_str_list[0]
decimal_part = None if len(number_str_list) == 1 else number_str_list[1]

#2.为整数部分添加千分位
new_integer_part = ''
reversed_integer_part = integer_part[::-1] # 将字符串左右反转
for i, c in enumerate(reversed_integer_part): # 遍历字符，每隔3个字符加逗号
    if i > 0 and i%3 == 0:
        new_integer_part = new_integer_part + ',' + c 
    else:
        new_integer_part += c
new_integer_part = new_integer_part[::-1] # 将字符串左右反转

#3.将整数部分和小数部分整合

if decimal_part:
    print('添加千分位后数字变为', new_integer_part + '.' + decimal_part)
else:
    print('添加千分位后数字变为', new_integer_part)

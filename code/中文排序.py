# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:16:43 2022

@author: xiong
"""

from itertools import chain
from pypinyin import pinyin, Style


def to_pinyin(s):
    '''转拼音

    :param s: 字符串或列表
    :type s: str or list
    :return: 拼音字符串
    >>> to_pinyin('你好吗')
    'ni3hao3ma'
    >>> to_pinyin(['你好', '吗'])
    'ni3hao3ma'
    '''
    return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))


print(sorted(['美国', '中国', '日本']))  # 美m 中z 日r abcdefghijkl[m]nopq[r]stuvwsy[z]
# ['中国', '日本', '美国']
print(sorted(['美国', '中国', '日本'], key=to_pinyin))  # 美m 中z 日r abcdefghijkl[m]nopq[r]stuvwsy[z]
# ['美国', '日本', '中国']
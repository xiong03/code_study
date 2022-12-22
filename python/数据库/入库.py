# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 15:40:48 2022

@author: xiong
"""

import pandas as pd
import pymysql
import geopandas as gpd
from pandas import DataFrame
from sqlalchemy import create_engine
import re

# #用来判断table是否存在
# def table_exists(cour,year):
#     sql = "show tables;"
#     cour.execute(sql)
#     #获取所有table，并将table改为list类型
#     tables = [cour.fetchall()]
#     table_list = re.findall('(\'.*?\')',str(tables))
#     table_list = [re.sub("'",'',each) for each in table_list]
#     table_name = "all"+str(year)
#     if table_name in table_list:
#         return 1        #存在返回1
#     else:
#         return 0        #不存在返回0

# #用于删除table
# def controller(year, database, sql_name, pwd, host, port):
#     conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=database)
#     cour = conn.cursor()
#     sql = f"drop table `all{year}`"
#     cour.execute(sql)
#     print(f"The table all{year} data has been deleted")
    
def create_table(year, database, sql_name, pwd, host, port):
    """

    Args:
        year: int, 气象数据年份
        database: str, 数据库名称, 默认为meteodata
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306

    Returns:

    """
    #连接数据库
    conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=database)
    sql = f"CREATE table if not exists `all{year}` (Station Text,Year int,Month int,Day int,APRE real,DMXP real," \
          f" DMNP real, MTEM real,DMXT real,DMNT real,AVRH real,MNRH real, PREP real, MEWS real, MXWS real, DMWS real," \
          f" EXWS real,DEWS real, SOHR real,DATE Date, " \
          f"FLAG VARCHAR(40) primary key)ENGINE=InnoDB DEFAULT CHARSET = utf8"
    #用于创建表的sql语句
    cour = conn.cursor()
    try:
        #执行sql操作
        cour.execute(sql)
        conn.commit()
        print(f"create table all{year} successful")
    except:
        #如果表已经存在，就进行回滚操作，sql不会执行
        conn.rollback()
    #关闭数据库
    cour.close()
    conn.close()

def me_data_handle(data: DataFrame):
    """

    Args:
        data: DataFrame

    Returns:

    """
    columns = ['Station', 'Year', 'Month', 'Day', 'APRE', 'DMXP', 'DMNP', 'MTEM', 'DMXT', 'DMNT', 'AVRH', 'MNRH',
               'PREP', 'MEWS', 'MXWS', 'DMWS', 'EXWS', 'DEWS', 'SOHR', 'DATE', 'FLAG']
    data.columns = columns[:-2]
    data[['Year', 'Month', 'Day']] = data[['Year', 'Month', 'Day']].astype(int)
    data['Year'] = data['Year'].astype(str)
    data['Month'] = data['Month'].apply(lambda x: format(x, '02d')).astype(str)
    data['Day'] = data['Day'].apply(lambda x: format(x, '02d')).astype(str)
    data['DATE'] = data['Year'] + '-' + data['Month'] + '-' + data['Day']
    data['FLAG'] = data['Station'] + data['Year'] + data['Month'] + data['Day']
    data[['Year', 'Month', 'Day']] = data[['Year', 'Month', 'Day']].astype(int)
    data.drop_duplicates(subset=['Station', 'Year', 'Month', 'Day'], keep='first', inplace=True)
    return data

    
def me_data_import(filename: str, year: int, database='meteodata', sql_name='root', pwd='123456', host='localhost',
                   port=3306, cover=False):
    """

    Args:
        filename: str, 气象数据文件路径
        year: int, 气象数据年份
        database: str, 数据库名称, 默认为meteodata
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306
        cover:bool 用于进行是否覆盖已有数据

    Returns: None

    """
    
    # #连接数据库
    # conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=database)
    # cour = conn.cursor()
    # if table_exists(cour,year):
    #     #用于查询数据的sql语句
    #     sql = f"select * from `all{year}`"
    #     cour.execute(sql)
    #     #读取一行数据
    #     results = pd.DataFrame(cour.fetchall())
    #     #关闭数据库
    #     cour.close()
    #     conn.close()
    #     #通过判断数据库表中是否有数据来进行是否结束函数
    #     if not results.empty:
    #         #print(f"this table all{year} has already data")
    #         #删除已有表的函数：来确定你是否想覆盖原来的数据并且插入新的数据
    #         if cover:
    #             controller(year, database, sql_name, pwd, host, port)
    #         elif not cover:
    #             print(f"skip table {year} successfully")
    #             return
    
    import time
    conn = create_engine(f'mysql+pymysql://{sql_name}:{pwd}@{host}:{port}/{database}', encoding='utf8')
    create_table(year, database, sql_name, pwd, host, port)
    #将数据分成多个存入sql
    pieces = pd.read_csv(filename, header=None, chunksize=100000)
    zst = time.time()
    for i, data in enumerate(pieces):
        st = time.time()
        data = me_data_handle(data)
        data.to_sql(f'all{year}', conn, if_exists='append', index=False)
        print(f'{i*100000:06d}-{i*100000+len(data):06d},本次耗时:{time.time()-st:.2f}s,总耗时:{time.time()-zst:.2f}s',
              end='\r')
    print(f'{filename} import  success !!!, 总耗时:{time.time()-zst:.2f}s')

def station_import(filename: str, database='meteodata', sql_name='root', pwd='123456', host='localhost', port=3306):
    """

    Args:
        filename: str, 站点文件路径
        database: str, 数据库名称, 默认为meteodata
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306

    Returns: None

    """
    conn = create_engine(f'mysql+pymysql://{sql_name}:{pwd}@{host}:{port}/{database}', encoding='utf8')
    df = pd.read_csv(filename,header=None)
    df.columns = ['code', 'X', 'Y', 'elev', 'stationName', 'regionalName']

    df.to_sql('station', conn, if_exists='append', index=False)

    print('import station success !!!')

# import glob,os

# path = r"Z:\Monarch\数据库入库文件\气象数据\已入库\国内"
# txts = glob.glob(path+os.sep+"*.txt")
# years = range(1980,2021)
# for txt,year in zip(txts,years):
#     me_data_import(txt,year,"school","root","123456","localhost",3306)

path = r"Z:\Monarch\数据库入库文件\气象数据\已入库\国内\CH_1980.txt"
me_data_import(path,1980,"school","root","123456","localhost",3306)


# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 10:02:45 2022

@author: xiong
"""

import pandas as pd
import pymysql
import geopandas as gpd
import numpy as np
from pandas import DataFrame
from sqlalchemy import create_engine

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
    conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=database)
    sql = f"CREATE table if not exists `a{year}` (Station Text, DATE Date, Year int,Month int,Day int," \
          f"ACMH real, ACSH real, DAEV real, DAPR real, DASF real, DAWM real, DWPR real, EVAP real," \
          f"MDEV real, MDPR real, MDSF real, MDWM real, MNPN real, MXPN real, PGTM real, PRCP real," \
          f"PSUN real, SNOW real, SNWD real, TAVG real, TMAX real, TMIN real, TOBS real, TSUN real,"\
          f"WDF1 real, WDFG real, WDFM real, WDMV real, WESD real, WSF1 real, WSFG real, WSFM real,"\
          f"WT01 real, WT02 real, WT03 real, WT04 real, WT05 real, WT06 real, WT08 real, WT09 real,"\
          f"WT16 real, WT18 real, FLAG VARCHAR(40) primary key)ENGINE=InnoDB DEFAULT CHARSET = utf8"
    # sql = f"CREATE table if not exists `waiguo{year}` (Station Text,Year int,Month int,Day int,APRE real,DMXP real," \
    #       f" DMNP real, MTEM real,DMXT real,DMNT real,AVRH real,MNRH real, PREP real, MEWS real, MXWS real, DMWS real," \
    #       f" EXWS real,DEWS real, SOHR real,DATE Date, " \
    #       f"FLAG VARCHAR(40) primary key)ENGINE=InnoDB DEFAULT CHARSET = utf8"
    cour = conn.cursor()
    try:
        cour.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    
def my_data_handle(data):
    """

    Args:
        data: DataFrame

    Returns:

    """
    
    #需要的数据
    # columns = ['Station']
    
    data = data.iloc[:,0:4]
    data.columns = ['Station','DATE','Types','Data']
    # data1.drop_duplicates(subset=['Station','DATE','Types'], keep='first', inplace=True)
    
    #将types为列名
    df = data.pivot(index=['Station','DATE'], columns=['Types'], values=['Data'])
    df.columns = df.columns.levels[1]
    
    
    #将station，date重新返回列中
    df.reset_index(inplace=True)
    df['DATE'] = df['DATE'].astype(str)
    df['FLAG'] = df['Station']+df['DATE']
    df['DATE'] = df['DATE'].astype(int)
    
    #用于计算year，month，day
    df_S_D = df[['Station', 'DATE']].copy()
    df_S_D['Year'] = df_S_D['DATE']//10000
    df_S_D['Month'] = (df_S_D['DATE']%10000)//100 
    df_S_D['Day'] = df_S_D['DATE']%100
    
    #合并
    result = df_S_D.merge(df, how = 'left', on=['Station','DATE'])
    
    #用于计算date，flag
    df_S_D[['Year', 'Month', 'Day']] = df_S_D[['Year', 'Month', 'Day']].astype(str)
    result['DATE'] = df_S_D['Year'] + '-' + df_S_D['Month'] + '-' + df_S_D['Day']
    result.drop_duplicates(subset=['Station', 'Year', 'Month', 'Day'], keep='first', inplace=True)
    result.replace(np.nan,32766,inplace=True)
    
    #获取需要的数据
    # result = result[[columns]]
    
    return result
    
def me_data_import(filename: str, year: int, database='meteodata', sql_name='root', pwd='123456', host='localhost',
                   port=3306):
    """

    Args:
        filename: str, 气象数据文件路径
        year: int, 气象数据年份
        database: str, 数据库名称, 默认为meteodata
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306

    Returns: None

    """
    import time
    conn = create_engine(f'mysql+pymysql://{sql_name}:{pwd}@{host}:{port}/{database}', encoding='utf8')
    create_table(year, database, sql_name, pwd, host, port)
    pieces = pd.read_csv(filename, header=None, chunksize=100000)
    zst = time.time()
    for i, data in enumerate(pieces):
        st = time.time()
        data = my_data_handle(data)
        try:
            data.to_sql(f'a{year}', conn, if_exists='append', index=False)
        except:
            pass
        print(f'{i*100000:06d}-{i*100000+len(data):06d},本次耗时:{time.time()-st:.2f}s,总耗时:{time.time()-zst:.2f}s',
              end='\r')
    print(f'{filename} import  success !!!, 总耗时:{time.time()-zst:.2f}s')

    
if __name__ == '__main__':
    path = r"D:\python\数据库\1980.csv"
    # pieces = pd.read_csv(path, header=None, chunksize=100000)
    # for i, data in enumerate(pieces):
    #     data = my_data_handle(data)
    
    me_data_import(path, 1980, 'school', 'root', '123456', 'localhost', 3306)

    
    
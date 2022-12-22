# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 21:13:12 2022

@author: xiong
"""

import pandas as pd
import pymysql



def get_data_by_stations(stations: list, types: list, start_time: str, end_time: str, db: str, sql_name='root',
                         pwd='123456', host='localhost', port=3306, time_merge=False):
    """

    Args:
        stations: list, 要获取的站点列表
        types: list, 要获取的气象要素列表
            |APRE: 平均本站气压 | DMXP:日最高本站气压 | DMNP: 日最低本站气压 | MTEM: 平均气温 | DMXT: 日最高气温|
            |DMNT: 日最低气温 | AVRH: 平均相对湿度 | MNRH: 最小相对湿度 | PREP: 降水量 | MEWS: 平均风速 |
            |MXWS: 最大风速|DMWS: 最大风速的风向|EXWS: 极大风速|DEWS: 极大风速的风向|SOHR: 日照时数|
        start_time: str, 开始时间，年-月-日格式
        end_time: str, 结束时间，年-月-日格式
        db: str, 连接的数据库名称
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306
        time_merge: bool, 导出数据时的时间格式，Ture时为年月日分开，False时为YYYY-mm-DD, 默认为False

    Returns:
        data: DataFrame, 形式为 站点 时间 要素
    """
    import time
    if time_merge:
        date = "DATE"
    else:
        date = "Year, Month, Day"
    conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=db)
    start_year = int(start_time.split('-')[0])
    end_year = int(end_time.split('-')[0])
    if len(end_time.split('-')) > 1:
        end_year += 1
    data = []
    zst = time.time()
    for year in range(start_year, end_year):
        sql = f'select Station, {date}, {",".join(types)} from all{year} where ' \
              f'Station in ({str(stations).strip("[]")}) and DATE >= "{start_time}" and DATE <= "{end_time}"'
        df = pd.read_sql(sql, conn)
        data.append(df)
        p = (year-start_year+1)/(end_year-start_year)
        t = time.time() - zst
        st = t/p - t
        print(f'{p*100:.2f}%, 耗时:{t:.2f}s, 还需:{st:.2f}', end='\r')
    print(f'{db} export  success !!!, 总耗时:{time.time() - zst:.2f}s')
    data = pd.concat(data)
    return data

def get_station_by_xy(x, y, db: str, sql_name='root', pwd='123456', host='localhost', port=3306):
    """

    Args:
        x: 经度范围
        y: 维度范围
        db: str, 连接的数据库名称
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: str, 数据库主机ip地址, 默认localhost
        port: int, 数据库端口, 默认3306

    Returns:

    """
    conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=db)
    sql = f"select `code`, `X`, `Y`, `elev`, `stationName` from station where Y between {y[0]} and {y[1]} and" \
          f" X between {x[0]} and {x[1]}"
    station = pd.read_sql(sql, conn)
    conn.close()
    return station

def get_data_by_xy(x, y, types: list, start_time: str, end_time: str, db: str, sql_name='root', pwd='123456',
                    host='localhost', port=3306, time_merge=False):
    """

    Args:
        x: 经度范围
        y: 维度范围
        types: list, 要获取的气象要素列表
            |APRE: 平均本站气压 | DMXP:日最高本站气压 | DMNP: 日最低本站气压 | MTEM: 平均气温 | DMXT: 日最高气温|
            |DMNT: 日最低气温 | AVRH: 平均相对湿度 | MNRH: 最小相对湿度 | PREP: 降水量 | MEWS: 平均风速 |
            |MXWS: 最大风速|DMWS: 最大风速的风向|EXWS: 极大风速|DEWS: 极大风速的风向|SOHR: 日照时数|
        start_time: str, 开始时间
        end_time: str, 结束时间
        db: str, 连接的数据库名称
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: str, 数据库主机ip地址, 默认localhost
        port: int, 数据库端口, 默认3306
        time_merge: bool, 导出数据时的时间格式，False时为年月日分开，True时为YYYY-mm-DD, 默认为False

    Returns:

    """
    station = get_station_by_xy(x, y, db, sql_name, pwd, host, port)
    code_sta = station['code'].tolist()
    data = get_data_by_stations(code_sta, types, start_time, end_time, db=db, host=host, port=port, sql_name=sql_name,
                                pwd=pwd, time_merge=time_merge)
    return data

def fun():
    x = [113.5716667,118.4822222]
    y = [24.48722222,30.07861111]
    types = ["PREP"]
    start_time = '2008-2-1'
    end_time = '2008-3-12'
    db = 'meteodata'
    sql_name = 'root'
    pwd = '123456'
    host = '192.168.118.158'
    
    # host = '192.168.31.76'
    
    port = 3306
    data = get_data_by_xy(x, y, types, start_time, end_time, db, sql_name, pwd, host, port)
    return data

if __name__ == "__main__":
    data = fun()

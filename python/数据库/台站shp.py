# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 22:06:22 2022

@author: xiong
"""

import pandas as pd
import pymysql
import geopandas as gpd


def creat_station_geopandas(db: str, sql_name='root', pwd='123456', host='localhost', port=3306, roi_shp=None):
    """

    Args:
        db: str, 数据库名称, 默认为meteodata
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306
        roi_shp:
    Returns:
        data: GeoDataFrame

    """
    conn = pymysql.connect(host=host, password=pwd, port=port, user=sql_name, db=db)
    if roi_shp:
        roi_df = gpd.read_file(roi_shp).to_crs('EPSG:4326')
        bounds = roi_df.geometry.bounds
        minx = bounds.minx.min()
        miny = bounds.miny.min()
        maxx = bounds.maxx.max()
        maxy = bounds.maxy.max()
        sql = f"select code,stationName,Y,X,elev from `station` " \
              f"where X between {minx} and {maxx} and Y between {miny} and {maxy}"
    else:
        sql = f"select code,stationName,Y,X,elev from `station`"
    df = pd.read_sql(sql, conn)
    data = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X, df.Y), crs='EPSG:4326')
    data.columns = ['Code', 'Station', 'Lat', 'Lon', 'elev', 'geometry']
    data[['Lat', 'Lon', 'elev']] = data[['Lat', 'Lon', 'elev']].astype(float)
    conn.close()
    return data

def creat_station_shp(path: str, sql_name='root', pwd='123456', host='localhost', port=3306):
    """

    Args:
        path: shapefile文件生成路径
        sql_name: str, mysql数据库用户名, 默认root
        pwd: str,  mysql数据库密码, 默认123456
        host: int, 数据库主机ip地址, 默认localhost
        port: str, 数据库端口, 默认3306

    Returns:

    """
    f_names = ['ChinaStations.shp', 'ForeignStations.shp']
    dbs = ['meteodata', 'meteodata_extens']
    for f_name, db in zip(f_names, dbs):
        data = creat_station_geopandas(db, sql_name, pwd, host, port)
        data.to_file(f'{path}/{f_name}', encoding='utf-8')
        print(f"{f_name} creat success !!!")
    gdf = pd.concat([gpd.read_file(f'{path}/{shp}') for shp in f_names]).pipe(gpd.GeoDataFrame)
    gdf.to_crs('EPSG:4326')
    gdf.to_file(f'{path}/tStations.shp', encoding='utf-8')
    
if __name__ == "__main__":
    path = r"D:\python\数据库\shp"
    creat_station_shp(path, sql_name='root', pwd='123456', host='192.168.118.158', port=3306)
    

    
    
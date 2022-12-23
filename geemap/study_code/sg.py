# -*- coding:utf-8 _*-
"""
@version:
author:Monarch
@time: 2021/07/19
@file: user_gee.py
@function:
@modify:
"""
import ee


def savitzky_golay(y: ee.List, window_size: int, order: int, deriv=0) -> ee.List:
    """
    基于List的sg滤波处理
    Args:
        y: ee.List, 原始数据
        window_size: int, 窗口大小
        order: int, 多项式阶数, 必须小于window_size
        deriv: int, 求导数的阶数, 默认为0

    Returns: ee.List, 滤波后的数据

    """
    half_window = (window_size - 1) / 2
    order_range = ee.List.sequence(0, order)
    k_range = ee.List.sequence(-half_window, half_window)
    b = ee.Array(k_range.map(lambda k: order_range.map(lambda o: ee.Number(k).pow(o))))
    m_pi = ee.Array(b.matrixPseudoInverse())
    impulse_response = (m_pi.slice(**{'axis': 0, 'start': deriv, 'end': deriv + 1 })).project([1])
    y0 = y.get(0)
    first_filling = y.slice(1, half_window + 1).reverse().map(
        lambda e: ee.Number(e).subtract(y0).abs().multiply(-1).add(y0))
    y_end = y.get(-1)
    last_filling = y.slice(-half_window - 1, -1).reverse().map(
        lambda e: ee.Number(e).subtract(y_end).abs().add(y_end))
    y_ext = first_filling.cat(y).cat(last_filling)
    run_length = ee.List.sequence(0, y_ext.length().subtract(window_size))
    smooth = run_length.map(
        lambda i: ee.Array(y_ext.slice(ee.Number(i), ee.Number(i).add(window_size))).multiply(impulse_response).reduce("sum", [0]).get([0])
    )
    return smooth


def sg_images(images: ee.ImageCollection, window_size: int, order: int, deriv=0) -> list:
    """
    基于影像的sg滤波处理
    Args:
        images: ee.ImageCollection, 需要处理的影像集, 注意请影像集中的每张影像的波段应处理为只有一个波段
        window_size: int, 窗口大小
        order: int, 多项式阶数, 必须小于window_size
        deriv: int, 求导数的阶数, 默认为0

    Returns: list, 包含滤波处理后的image的list

    """
    half_window = (window_size - 1) / 2
    order_range = ee.List.sequence(0, order)
    k_range = ee.List.sequence(-half_window, half_window)
    b = ee.Array(k_range.map(lambda k: order_range.map(lambda o: ee.Number(k).pow(o))))
    m_pi = ee.Array(b.matrixPseudoInverse())
    impulse_response = (m_pi.slice(**{'axis': 0, 'start': deriv, 'end': deriv + 1})).project([1])
    y = images.sort('system:time_start', False).toBands().toArray()
    times = images.aggregate_array('system:time_start')
    ids = images.aggregate_array('system:id')
    band_name = images.first().bandNames().get(0).getInfo()
    y1 = images.sort('system:time_start', True).toBands().toArray()
    y0 = y1.arrayGet(0)
    first_filling = y.arraySlice(0, -half_window - 1, -1).subtract(y0).abs().multiply(-1).add(y0)
    y_end = y.arrayGet(0)
    last_filling = y.arraySlice(0, 1, half_window+1).subtract(y_end).abs().add(y_end)
    y_ext = first_filling.arrayCat(y1, 0).arrayCat(last_filling, 0)
    run_length = ee.List.sequence(0, images.size().subtract(1))
    smooth = []
    for i in run_length.getInfo():
        smooth.append(y_ext.arraySlice(0, ee.Number(i), ee.Number(i).add(window_size))
                      .multiply(impulse_response).arrayReduce("sum", [0]).arrayGet([0]).rename(band_name+f'_{i}')
                      .set({'system:time_start': times.get(i), 'system:id': ids.get(i)}))
    return smooth
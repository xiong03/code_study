import rasterio
import glob
import numpy as np
from scipy import stats
import time,os

data_2 = np.arange(2000, 2005, 1)
start = time.time()
file1 = r'D:\python\12 趋势和显著性\MAT/'
File1 = r't2000.tif'
a = []
b = []
with rasterio.open(file1 +os.sep+ File1) as src:  # 获取读取窗口
    windows = [window for ij, window in src.block_windows()]
    profile = src.profile
    nodata = src.nodata
write_file = ['prcp_slope.tif', 'prcp_pvalue.tif']
Data = []
for i in write_file:
    src1 = rasterio.open(r'D:\python\12 趋势和显著性\输出/' + i, 'w', **profile)
    Data.append(src1)

def fun2(data_1):
    """
    :param data_1: 需要计算趋势和显著性水平的数组
    :return: 返回趋势r2score和显著性水平pvalue
    """
    J = data_1.shape[1]
    K = data_1.shape[2]
    k = np.empty((2, 1, J, K), dtype='float32')
    for x in range(0, J):
        for y in range(0, K):
            y_data = data_1[:, x, y] / 10
            if len(y_data[y_data == nodata]) > 0:
                k[:, 0, x, y] = np.nan
            else:
                x_data = data_2
                OLS = stats.linregress(x_data, y_data)
                slope = OLS[0]
                pvalue = OLS[3]
                k[1, 0, x, y] = pvalue  # 显著性水平
                k[0, 0, x, y] = slope  # 趋势
    return k

def fun3(win):
    file = r'C:\Users\lwq\Desktop\趋势和显著性\文件\*'
    dat = []
    for year in range(2000, 2005):
        file2 = glob.glob(file + str(year) + '*.tif')
        with rasterio.open(file2[0]) as src1:
            block_array = src1.read(window=win)[0]  # 读取数据
        dat.append(block_array)
    data1 = np.array(dat)  # 处理数
    data2 = fun2(data1)
    Data[0].write(data2[0], window=win)
    Data[1].write(data2[1], window=win)

Data[0].close()
Data[1].close()
end = time.time()
print(end - start)

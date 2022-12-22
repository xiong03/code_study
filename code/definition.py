# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 15:34:13 2022

@author: xiong
"""

def fun(path, outpath):
    
    import requests
    import base64
    import time
    import socket
    
    socket.setdefaulttimeout(20)
    
    '''
    图像清晰度增强
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())
     
     
    params = {"image":img}
    access_token = '24.838af13c553da34e7d27dc33b51b8bfa.2592000.1662449628.282335-26936261'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print (response.json()['image'])
        print(f'successful {path}')
        
    imgdata = base64.b64decode(response.json()["image"])
    response.close()
    file = open(outpath, 'wb')
    file.write(imgdata)
    file.close()
    
    time.sleep(1)
    
    
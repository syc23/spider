#!usr/bin/env python  
#-*- coding:utf-8 -*-
from jsonpath import jsonpath
from aip import AipOcr
def captcha_recognize(img_path):
    APP_ID = '17212972'
    API_KEY = 'qdv8ZiTG0um15DlaWL8eKow7'
    SECRET_KEY = 'TVGTXMlPDKO62MBSvhnrSMDniG2VjL27'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    image = get_file_content(img_path)
    """ 调用通用文字识别, 图片参数为本地图片 """
    client.basicGeneral(image);
    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    code, = jsonpath(client.basicAccurate(image),'$..words')
    return code
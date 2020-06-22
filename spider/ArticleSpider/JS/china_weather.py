#!usr/bin/env python
#-*- coding:utf-8 -*-
import execjs
import requests
import json,jsonpath
from fake_useragent import FakeUserAgent
class get_weather_data():
    def __init__(self):
        self.headers = {
            'User-Agent':FakeUserAgent().random,
        }
        self.url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
    def getParam(self):
        method = 'GETDETAIL'
        city = '贵阳'
        type = 'HOUR'
        startTime = '2019-10-07 08:00'
        endTime = '2019-10-08 11:00'
        js = execjs.compile(open('./china_weather.js',encoding='utf-8').read())
        # 两种函数执行方式
        # params = js.eval('getParams("{}","{}","{}","{}","{}")'.format(method,city,type,startTime,endTime))
        # 函数调用时不需要使用元组的方式
        params = js.call('getParams',method,city,type,startTime,endTime)
        return params
    def get_data(self):
        data = {
            'd':self.getParam()
        }
        data_ = requests.post(self.url,data=data,headers=self.headers).text
        js = execjs.compile(open('./china_weather.js',encoding='utf-8').read())
        data_ = js.call('decodeData',data_)
        print(data_)
if __name__ == '__main__':
    weather_data = get_weather_data()
    # weather_data.getParam()
    weather_data.get_data()

#!usr/bin/env python
#-*- coding:utf-8 -*-
import requests
from fake_useragent import UserAgent

def get_content():
    headers = {
        'User-Agent': UserAgent().random
    }
    for i in range(1, 2):
        data = {
            "t": 0,
            "pindex": i,
            "size": 20,
            "MethodName": "BoxOffice_GetHisbestInland"
        }
        response = requests.post("http://www.endata.com.cn/API/GetData.ashx",data=data,headers=headers)
        content = response.json()
        for item in content['Data']['Table']:
            line = ",".join(map(str, item.values()))
            print(line)

if __name__ == '__main__':
    get_content()
#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import re
import js2py
import execjs
url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg=110000'
headers = {
    # 'Referer': 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html',
    'Cookie': '__jsluid_h=4f673734688f4bece0391cb8c24f7f53; __jsl_clearance=1568010495.736|0|UK4bUvFbDO4iJGft55ZTeNckt%2BA%3D; SECTOKEN=6942333103442234923; UM_distinctid=16d14b57522605-0e3aa6437c6cea-e343166-1fa400-16d14b575237b6; CNZZDATA1261033118=1566550996-1568005675-http%253A%252F%252Fwww.gsxt.gov.cn%252F%7C1568005675; JSESSIONID=2981D9121CB800A22F7D62F652276EC8-n1:0; tlb_cookie=S172.16.12.67',
    'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
data = {
    'start': '0',
    'length': '10'
}
response = requests.post(url,headers=headers,data=data)
print(response.content.decode())
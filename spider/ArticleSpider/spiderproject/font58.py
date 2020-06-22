#!usr/bin/env python  
#-*- coding:utf-8 -*-
"""
    58字体反爬
"""
import requests
import re
from fake_useragent import UserAgent
import base64
from fontTools.ttLib import TTFont
from io import BytesIO
import parsel

headers = {
    'User-Agent':UserAgent().random
}

url = 'https://qn.58.com/searchjob/'

response = requests.get(url,headers=headers)
response.encoding=response.apparent_encoding

content = response.text

fontb64, = re.findall(r'.*base64,(.*?)\).*',content,re.S)
font_content = base64.b64decode(fontb64)

coordinatetofont = {
    (1588,0):'男',(0,144):'经',(770,0):'中',(868,0):'王',(0,1026):'M',(746,0):'士',(230,390):'硕',
    (0,-508):'周',(825,367):'大',(928,0):'生',(0,-227):'5',(-764,0):'杨',(156,262):'赵',(0,1549):'B',
    (784,0):'无',(0,410):'0',(1298,0):'高',(146,78):'应',(924,0):'李',(582,0):'届',(-52,-52):'本',
    (0,134):'8',(238,0):'张',(660,0):'黄',(0,132):'技',(159,-123):'3',(210,358):'校',(0,125):'2',
    (-110,-150):'女',(-121,62):'6',(228,306):'科',(1460,0):'吴',(0,1325):'1',(299,0):'陈',
    (164,0):'以',(0,-1023):'4',(128,-74):'9',(-46,-550):'验',(1944,0):'下',(265,-118):'专',
    (-221,0):'A',(-74,-366):'刘',(-244,-426):'7',(0,110):'博',(-833,0):'E'
}
tf = TTFont(BytesIO(font_content))
font_map = {}
for i in tf.getGlyphNames()[1:-1]:
    tmp = tf['glyf'][i].coordinates
    x1,y1 = tmp[0]
    x2,y2 = tmp[1]
    xx = (x2-x1,y2-y1)
    key = i.replace("uni","&#x").lower()
    font_map[key] = coordinatetofont[xx]

for key,value in font_map.items():
    content = content.replace(key+";",value)
with open('./font/test.html','w',encoding='utf-8') as f:
    f.write(content)
res = parsel.Selector(content)
name = res.xpath('//div[@class="tablist"]//dl//dd[contains(@class,"w70")]/text()').getall()
gender = res.xpath('//div[@class="tablist"]//dl//dd[contains(@class,"w48")]/text()').getall()
age = res.xpath('//div[@class="tablist"]//dl//dd[contains(@class,"w60")]/text()').getall()
workexperience = res.xpath('//div[@class="tablist"]//dl//dd[contains(@class,"w80")]/text()').getall()
education = res.xpath('//div[@class="tablist"]//dl//dd[contains(@class,"w90")]/text()').getall()
position = res.xpath('//div[@class="tablist"]//dl//dd[contains(@class,"w108")]/text()').getall()

for i in zip(name,gender,age,workexperience,education,position):
    tmp = list(i)
    print(tmp)






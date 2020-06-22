import requests
import re
import base64
import parsel
import io
from lxml import etree
from fontTools.ttLib import TTFont
"""
    破解字体反爬
"""
url = r'https://sz.58.com/chuzu/'
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
response = requests.get(url=url,headers=headers)
response.encoding = 'utf-8'
# 获取加密字符串
base64_str = re.findall(r"url\('.*base64,(.*?)'\) format",response.text,re.S)[0]
b = base64.b64decode(base64_str)
font = TTFont(io.BytesIO(b))
bestcmap = font['cmap'].getBestCmap()
newmap = {}
for key in bestcmap.keys():
    value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
    key = hex(key)
    key_ = key.replace('0x','&#x') + ';'
    newmap[key_] = value
# 把页面上自定义字体替换成正常字体
response_ = response.text
for key,value in newmap.items():   
    if key in response_content:
        response_ = re.sub(key,str(value),response_)
# 获取标题
sel = parsel.Selector(response_)
lis = sel.xpath('//ul[@class="house-list"]/li')
for li in lis:
    price = li.xpath('.//b[@class="strongbox"]/text()').get().strip()
    name = li.xpath('.//a[@class="strongbox"]/text()').get().strip()
    url = li.xpath('.//a[@class="strongbox"]/@href').get()
    type_ = li.xpath('.//p[@class="room"]/text()').get().strip()
    if price and name and url and type_ :
        print(url,type_,name,price)
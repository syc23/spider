#!usr/bin/env python  
#-*- coding:utf-8 -*-
"""
    猫眼字体反爬(UNICODE不同，字形相同，坐标相同，根据坐标求得相对应的字形)
"""
import requests
import re
from fake_useragent import UserAgent
import base64
from fontTools.ttLib import TTFont
import parsel
import matplotlib.pyplot as plt
import hashlib

maoyan1 = TTFont('./font/maoyan1.woff')
maoyan2 = TTFont('./font/maoyan2.woff')
unicode_value = {
    "uniE291":"0",
    "uniE785":"7",
    "uniE834":"2",
    "uniED2F":"4",
    "uniEE19":"3",
    "uniEEEE":"8",
    "uniEF66":"9",
    "uniF0FC":"5",
    "uniF5FB":"1",
    "uniF7D7":"6"
}
coor_unicode = {}

for i in maoyan1.getGlyphNames()[1:-1]:
    tmp = maoyan1['glyf'][i].coordinates
    hs = hashlib.md5()
    hs.update(str(list(tmp)).encode("utf-8"))
    hashvalue = hs.hexdigest()
    coor_unicode[hashvalue] = i

coor_value = {}

for key,value in coor_unicode.items():
    coor_value[key] = unicode_value[value]

coorhash_unicode = {}
for i in maoyan2.getGlyphNames()[1:-1]:
    tmp = maoyan2['glyf'][i].coordinates
    hs = hashlib.md5()
    hs.update(str(list(tmp)).encode("utf-8"))
    keys = hs.hexdigest()
    coorhash_unicode[keys] = i

unicodetovalue = {}

for key,value in coorhash_unicode.items():
    unicodetovalue[value] = coor_value[key]

# 最终根据坐标的hash编码，求得相对应的字形
print(unicodetovalue) # hashvalue --> 1 or 2 0r 3 ............








#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import re
import parsel
from selenium import webdriver
from fake_useragent import FakeUserAgent
import time
url = 'https://zu.fang.com/house/a21/'
def get_content(link):
    headers = {
        'User-Agent': FakeUserAgent().random
    }
    response = requests.get(link, headers=headers)
    response.encoding = 'utf-8'
    print(response.request.url)
    print(response.status_code)
    content = response.text
    print(content)
    name = re.findall(r" agentName:'(.*?)',",content,re.S)
    print(name)
def get_link():
    headers = {
        'User-Agent':FakeUserAgent().random
    }
    response = requests.get(url,headers=headers)
    response.encoding = 'gb2312'
    content = response.text
    sel = parsel.Selector(content)
    link = sel.xpath('//div[@class="houseList"]/dl/dd[@class="info rel"]/p[@class="title"]/a/@href').getall()[6:]
    for i in link:
        # urls = 'https://zu.fang.com'+i
        urls = 'http://search.fang.com/captcha-b64c3c4d4e3190bb69/redirect?h=https://zu.fang.com/chuzu/1_61211134_-1.htm'
        get_content(urls)
        break
get_link()
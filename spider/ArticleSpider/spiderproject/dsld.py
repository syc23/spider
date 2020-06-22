#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
from fake_useragent import FakeUserAgent
from urllib import parse
import re
base_url = 'http://www.dianshangleida.com/'
# url = 'http://www.dianshangleida.com/'
# headers = {
#     'User-Agent':FakeUserAgent().random
# }
#
# response = requests.get(url,headers=headers)
# response.encoding = response.apparent_encoding
#
# sel = parsel.Selector(response.text)
#
# link = sel.xpath('//a[text()="查看更多"]/@href').getall()
# link = ['http://www.dianshangleida.com'+ i for i in link]
detail = 'http://www.dianshangleida.com/list/appeal/'
def get_html(url):
    headers = {
        'User-Agent': FakeUserAgent().random
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    sel = parsel.Selector(response.text)
    return sel
def get_detail(url):
    headers = {
        'User-Agent':FakeUserAgent().random
    }
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    sel = parsel.Selector(response.text)

    detail_url_list = sel.xpath('//ul[@id="tam_newlist"]/li/a/@href').getall()
    for i in detail_url_list:
        detail_url = parse.urljoin(base_url,i)
        content = get_html(detail_url)
        name = content.xpath('//h2[@class="person_top_tt1"]/text()').get()
        name = re.findall('【.*】(.*?)举报信息',name)
        if name:
            print(name[0].strip())
        con = content.xpath('//div[@class="commentList"]/table/tbody/tr')
        for i in con:
            con = i.xpath('./td/text()').getall()
            print('|'.join(con))
        print('*'*50)
    next_url = sel.xpath('//a[text()="下一页"]/@href').get()
    next_url = parse.urljoin(base_url,next_url)
    if next_url:
        print(next_url)
        get_detail(next_url)
get_detail(detail)
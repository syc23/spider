#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
from lxml import etree
from multiprocessing import pool
# 使用进程池,爬取猫眼电影
def get_content(url):
     headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
     }
     html = requests.get(url,headers=headers).content.decode('utf-8')
     contents = etree.HTML(html)
     parse_html(contents)
def parse_html(contents):
    item = {}
    title = contents.xpath('//p[@class="name"]/a/text()')
    href = contents.xpath('//p[@class="name"]/a/@href')
    releasetime = contents.xpath('//p[@class="releasetime"]/text()')
    for i,j,k in zip(title,href,releasetime):
        item['title'] = i
        item['href'] = 'https://maoyan.com'+j
        item['releasetime'] = k
        print(item)
    print("*"*40)
if __name__ == '__main__':
    po = pool.Pool()
    po.map(get_content, ['https://maoyan.com/board/4?offset={}'.format(temp) for temp in range(0,100,10)])
    # for i in range(0,100,10):
    #     po.apply_async(get_content,args=('https://maoyan.com/board/4?offset={}'.format(i),))
    # po.close()
    # po.join()
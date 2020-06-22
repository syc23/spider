#!usr/bin/env python  
#-*- coding:utf-8 -*-
# 多线程+队列实现爬取时光网
from gevent import monkey
monkey.patch_all()
from gevent.queue import Queue
import parsel
import requests, csv, gevent
flag = True
link = Queue()
link.put_nowait('http://www.mtime.com/top/tv/top100/')
for n in range(2, 11):
    url = 'http://www.mtime.com/top/tv/top100/index-%d.html' % n
    link.put_nowait(url)

def deal_info(value):
    if value:
        return value
    else:
        return ''


def crawler():
    while not link.empty():
        url = link.get_nowait()
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        mvs = sel.xpath('//ul[@id="asyncRatingRegion"]/li')
        for mv in mvs:
            title = mv.xpath('.//div[@class="mov_con"]/h2/a/text()').get()
            director = mv.xpath('.//div[@class="mov_con"]/p[position()<2]/a/text()').get()
            actor1 = mv.xpath('.//div[@class="mov_con"]/p[position()=2]/a[1]/text()').get()
            actor2 = mv.xpath('.//div[@class="mov_con"]/p[position()=2]/a[2]/text()').get()
            introduction = mv.xpath('./div[@class="mov_con"]/p[@class="mt3"]/text()').get()
            title = deal_info(title)
            director = deal_info(director)
            actors = deal_info(actor1) + ' ' + deal_info(actor2)
            introduction = deal_info(introduction)
            print(title, director, actors, introduction)
            writer.writerow([title, director, actors, introduction])

f = open(r'./mv.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(f)
if flag ==True:
    writer.writerow(['剧名', '导演', '主演', '简介'])
    flag = False
tasks_list = [gevent.spawn(crawler) for i in range(5)]
gevent.joinall(tasks_list)

f.close()
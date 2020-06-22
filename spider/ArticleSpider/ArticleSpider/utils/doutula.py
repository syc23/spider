#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import time
import re
from lxml import etree
import os
import threading
from urllib import request
from queue import Queue
# 实现多线程爬虫
class Procuder(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.spider(url)
    def spider(self,url):
        try:
            time.sleep(0.5)
            html = requests.get(url, headers=self.headers,timeout=3).content.decode("utf-8")
            text = etree.HTML(html)
            img_list = text.xpath('//a[contains(@class,"col-xs-6")]')
            for i in img_list:
                img_url = i.xpath('./img/@data-original')[0]
                alt = i.xpath('./img/@alt')[0].strip()
                alt = re.sub('[\.\*\?？。，,!！\+~…【】\(\)（）\s]', '', alt).strip()
                if alt == '':
                    alt = re.split('\.', re.split('\/', img_url)[-1])[0]
                suffix = os.path.splitext(img_url)[-1]
                filename = alt + suffix
                self.img_queue.put((img_url,filename))
        except:
            print("********************服务器未响应，页面加载失败！*************************")

class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.img_queue.empty() or self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get()
            try:
                request.urlretrieve(img_url,'imgs/'+filename)
            except:
                print("*********************服务器未响应，{}下载失败！*******************".format(filename))
            print(filename  +'下载完成！')
def main():
    page_queue = Queue(2600)
    img_queue = Queue(10000)
    for i in range(1,2594):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(i)
        page_queue.put(url)
    for i in range(8):
        t = Procuder(page_queue,img_queue)
        t.start()
    for i in range(10):
        t = Consumer(page_queue, img_queue)
        t.start()

if __name__ == '__main__':
    main()
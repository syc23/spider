#!usr/bin/env python  
#-*- coding:utf-8 -*-
from queue import Queue
from threading import Thread
import requests
from fake_useragent import UserAgent
import parsel
# 爬虫类
class CrawlInfo(Thread):
    def __init__(self,url_queue,html_queue):
        self.url_queue = url_queue
        self.html_queue = html_queue
        Thread.__init__(self)
    def run(self):
        headers = {
            'User-Agent': UserAgent().random,
        }
        while self.url_queue.empty() == False:
            response = requests.get(self.url_queue.get(),headers=headers)
            if response.status_code==200:
                self.html_queue.put(response)
# 解析类
class ParseInfo(Thread):
    def __init__(self,html_queue):
        self.html_queue = html_queue
        Thread.__init__(self)
    def run(self):
        while self.html_queue.empty() == False:
            response = self.html_queue.get()
            response.encoding = 'utf-8'
            sel = parsel.Selector(response.text)
            divs = sel.xpath('//div[contains(@class,"article")]')
            with open(r'./qiushi.txt','a',encoding='utf-8') as f:
                for div in divs:
                    content = div.xpath('string(.//div[@class="content"])').get().strip()
                    f.write(content+'\n')
if __name__ == '__main__':
   base_url = 'https://www.qiushibaike.com/text/page/{}/'
   url_queue = Queue()
   html_queue = Queue()
   for url in [base_url.format(num) for num in range(1,14)]:
       url_queue.put(url)

   crawl_list = []
   for i in range(3):
       crawl1 = CrawlInfo(url_queue,html_queue)
       crawl_list.append(crawl1)
       crawl1.start()
   for crawl in crawl_list:
       crawl.join()

   crawl2 = ParseInfo(html_queue)
   crawl2.start()

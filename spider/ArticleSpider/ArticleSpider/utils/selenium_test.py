#!usr/bin/env python  
#-*- coding:utf-8 -*-
from  selenium import webdriver
from lxml import etree
import time
import re
# 使用代理
# option = webdriver.ChromeOptions()
# option.add_argument('--proxy-server=http://1.192.245.236:9999')
# driver = webdriver.Chrome(chrome_options=option)
# driver.get('http://www.httpbin.org/ip')
index = 1
class lagou(object):
    def __init__(self):
        self.page_url ='https://www.zhipin.com/c101010100/?query=python&page=1&ka=page-1'
        # 设置无界面浏览器
        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome()
        self.positions=[]
    def spider(self,page_url):
        self.driver.get(page_url)
        source = self.driver.page_source
        html = etree.HTML(source)
        url_list = html.xpath('//div[@class="info-primary"]/h3/a/@href')
        for url in url_list:
            url = 'https://www.zhipin.com'+url
            self.parse_detail(url)
        if source.find('next disabled') == -1:
            next_page_url = 'https://www.zhipin.com'+html.xpath('//a[@class="next"]/@href')[0]
            self.spider(next_page_url)

    def parse_detail(self,url):
        self.driver.execute_script("window.open('{}')".format(url))
        self.driver.switch_to_window(self.driver.window_handles[1])
        self.driver.get(url)
        source = self.driver.page_source
        html = etree.HTML(source)
        # title = html.xpath('//h2[@class="name"]/text()')[0]
        salary = html.xpath('//span[@class="salary"]/text()')[0]
        # requirment = html.xpath('//dd[@class="job_request"]//h3/span/text()')
        # requirment = ','.join(requirment)
        # req = re.sub('[/\s]','',requirment)
        # position = {
        #     'title':title,
        #     'salary':salary,
        #     'requirment':req
        # }
        # self.positions.append(position)
        global index
        print(salary)
        print(index)
        index+=1
        print("*"*30)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])


if __name__ == '__main__':
    lg = lagou()
    lg.spider('https://www.zhipin.com/c101010100/?query=python&page=1&ka=page-1')

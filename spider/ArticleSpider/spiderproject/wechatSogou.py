#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
import random
class sogou(object):
    def __init__(self):
        self.base_url = 'https://weixin.sogou.com/weixin'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        proxy = [
            '116.62.198.43:8080','193.93.78.132:32231'
        ]
        self.proxys = {
            'http': random.choice(proxy)
        }
    def article(self,url):
        data = {
            'type':'2',
            's_from':'input',
            'query':'一加',
            'ie':'utf8',
            '_sug_':'n',
            '_sug_type_':''
        }
        response = requests.get(url,headers = self.headers,data=data,proxies=self.proxys)
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        article_link = sel.xpath('//div[@class="txt-box"]/h3/a/@data-share').getall()
        print(response.text)
        # for link in article_link:
        #     self.getcontent(link)
        # next_url = sel.xpath('//a[@id="sogou_next"]/@href').get()
        # if next_url:
        #     next_url = self.base_url + next_url
        #     self.article(next_url)
        # else:
        #     return
    def getcontent(self,link):
        response =  requests.get(link,headers = self.headers,proxies=self.proxys)
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        title = sel.xpath('//h2[@id="activity-name"]/text()').get().strip()
        author = sel.xpath('//a[@id="js_name"]/text()').get().strip()
        pub_time = sel.re(r's="(\d+-\d+-\d+)"')[0]
        content = sel.xpath('//div[@id="page-content"]').getall()[0]
        print(title,author,pub_time)


if __name__ == '__main__':
    url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E4%B8%80%E5%8A%A0'
    so = sogou()
    so.article(url)
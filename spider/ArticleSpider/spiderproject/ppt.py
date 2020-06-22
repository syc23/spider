#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
from urllib import parse
from fake_useragent import FakeUserAgent
import os
class PPT():
    def __init__(self):
        self.headers = {
             'User-Agent':FakeUserAgent().random
        }
        self.start_url = 'http://www.ypppt.com/moban/'
    def parse_html(self,url):
        response = requests.get(url,headers=self.headers)
        response.encoding = response.apparent_encoding
        return response.text
    def get_ppt(self,url):
        sel = parsel.Selector(self.parse_html(url))
        detail_links = sel.xpath('//ul[@class="posts clear"]/li/a[@class="img_preview"]/@href').getall()
        for link in detail_links:
            link = 'http://www.ypppt.com'+link
            self.parse_download(link)
        翻页
        next_url = sel.xpath('//a[text()="下一页"]/@href').get()
        if next_url:
            next_url = parse.urljoin('http://www.ypppt.com/moban/',next_url)
            print(next_url)
            get_ppt(next_url)
        else:
            return
    def parse_download(self,link):
        sel = parsel.Selector(self.parse_html(link))
        download_url = 'http://www.ypppt.com' + sel.xpath('//a[@class="down-button"]/@href').get()
        sel = parsel.Selector(self.parse_html(download_url))
        load_url = sel.xpath('//a[text()="下载地址1"]/@href').get()
        load_url = parse.urljoin('http://www.youpinppt.com',load_url)
        name = sel.xpath('//div[@class="de"]/h1/text()').get()
        self.save_ppt(load_url,name)
    def save_ppt(self,link,name):
        content = self.parse_html(link).encode('utf-8')
        name = name.split('-')[0].strip()
        print('正在下载：{}'.format(name))
        file_path = os.path.join('./ppt_template',name+'.rar')
        with open(file_path,'wb') as f:
            f.write(content)
        print(name + '下载完成！')
if __name__== '__main__':
    ppt = PPT()
    ppt.get_ppt(ppt.start_url)
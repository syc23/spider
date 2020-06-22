#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
import re
import os
from multiprocessing import pool
class Lianai():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.start_url = 'https://www.puamap.com/lianai/index_1.html'
        self.base_url = 'https://www.puamap.com'
    def get_content(self,url,name,title):
        url = self.base_url+url
        response = requests.get(url,headers=self.headers)
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        article_content = ' '.join([re.sub(r'\r|\t|\u3000\u3000','',tmp) for tmp in sel.xpath('//div[@class="article_con"]//p/text()').getall()])
        self.save_data(title,name,article_content)
    def save_data(self,title,name,article_content):
        path = os.path.join('./aa',title)
        if not os.path.exists(path):
            os.makedirs(path)
            print('开始爬取{}类的文章'.format(title))
        save_path = os.path.join(path,name+'.txt')
        try:
            with open(save_path,'w',encoding='utf-8') as f:
                print(name,'正在爬取！')
                f.write(article_content)
        except Exception as e:
            print(e)

    def get_content_link(self,title,link):

        response = requests.get(link,headers=self.headers)
        response.encoding = response.apparent_encoding
        res_text = response.text
        groups = re.findall(r'<div class="left"><a href="(/lianai/.*?/\d+\.html)" title="(.*?)">',res_text,re.S)
        for url,name in groups:
            try:
                self.get_content(url,name,title)
            except:
                pass
        sel = parsel.Selector(res_text)
        next_url = sel.xpath('//ul[@class="pages"]//a[text()="下一页"]/@href').get()
        if next_url:
            print('正在爬取{}分类的第{}页'.format(title,next_url.split('_')[-1].split('.')[0]),'https://www.puamap.com/lianai/{}/'.format(response.url.split('/')[-2])+next_url)
            try:
                self.get_content_link(title,'https://www.puamap.com/lianai/{}/'.format(response.url.split('/')[-2])+next_url)
            except:
                pass
        else:
            pass

    def run(self):
        response = requests.get(self.start_url,headers=self.headers)
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        links = [self.base_url+tmp for tmp in sel.xpath('//dl[@class="news_classify"]/dd/a[position()>3]/@href').getall()]
        titles = sel.xpath('//dl[@class="news_classify"]/dd/a[position()>3]/text()').getall()
        for title,link in zip(titles,links):
            try:
                self.get_content_link(title,link)
            except:
                pass
if __name__ == '__main__':
    la = Lianai()
    try:
        la.run()
    except:
        pass
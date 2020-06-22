#!usr/bin/env python
#-*- coding:utf-8 -*-
from urllib import request
import requests,re,os
import parsel
class Baidupic():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        }
    def url_lsit(self):
        return ['http://tieba.baidu.com/f?kw=%E6%B1%BD%E8%BD%A6&ie=utf-8&pn={}'.format(i) for i in range(0,6000,50)]
    def parse_html(self,url):
       return requests.get(url,headers=self.headers).content.decode('utf-8')
    def save_pic(self,html_str):
        pic_url =re.findall(r'bpic="(.*?)"',html_str,re.S)
        for url in pic_url:
            pic_content = requests.get(url,headers=self.headers).content
            filename = os.path.join(r'D:\Tensorflow\retrain\data\train\house', url.split('/')[-1])
            print(filename)
            with open(filename,'wb') as f:
                f.write(pic_content)
    def run(self):
        urls = self.url_lsit()
        for url in urls:
            html_str = self.parse_html(url)
            self.save_pic(html_str)


if __name__ == '__main__':
    baidupic = Baidupic()
    baidupic.run()
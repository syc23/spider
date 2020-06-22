#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
import csv,xlwt
import re
import codecs
from multiprocessing import pool
class neiha():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
        }
    def parse_html(self,url):
        print(url)
        response = requests.get(url,headers=self.headers)
        response.encoding = response.apparent_encoding
        requestion_answer = re.findall(r'<h3><a href="/njjzw/\d+\.html" class="title" title=".*?">(.*?)</a></h3>.*?<div class="desc">(.*?)</div>',response.text,re.S)
        f = open('nahan.csv','a',encoding='utf-8',newline='')
        j = 0
        for i in requestion_answer:
           req,answer = i
           req = req.strip()
           answer = re.sub(r'\u3000|答案|&quot;0&quot;|：|: |:','',answer).strip()
           print('正在存储:',req)
           k = 0
           for data in (req,answer):
               sheet.write(j,k,data)
               k+=1
           j+=1
        #    writer = csv.writer(f)
        #    writer.writerow(list((req,answer)))
        # f.close()
        book.save('./neihaba.xls')

if __name__ == '__main__':
    urls = ['https://www.neihan8s.com/njjzw/index.html']
    for i in range(2,3):
        urls.append('https://www.neihan8s.com/njjzw/index_{}.html'.format(i))
    nhb = neiha()
    p = pool.Pool(6)
    p.map(nhb.parse_html,urls)
    # nhb.parse_html(url)
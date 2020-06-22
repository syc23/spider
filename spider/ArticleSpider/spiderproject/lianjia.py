#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
import csv
import re,time
import xlwt
from fake_useragent import FakeUserAgent
class Lianjia():
    def __init__(self):
        self.headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 '
            # 如果你没有安装这个库这话也可以使用上面的那个方法，主要是防反爬
            'User-Agent':FakeUserAgent().random
        }
    def get_html(self,url):
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            pass
        response.encoding = response.apparent_encoding
        return response.text

    def get_page_num(self,url):
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            pass
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        nump = sel.re(r'"totalPage":(\d+),')
        if nump:
            return nump[0]
        else:
            return None
    def get_link_page_num(self):
        url = 'https://qd.lianjia.com/ershoufang/'
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            pass
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        links = ['https://qd.lianjia.com'+link for link in sel.xpath('//div[@data-role="ershoufang"]/div/a/@href').getall()]
        for link in links[3:]:
            content = self.get_html(link)
            sel = parsel.Selector(content)
            for j in ['https://qd.lianjia.com'+i for i in sel.xpath('//div[@data-role="ershoufang"]/div[position()>1]//a/@href').getall()]:
                page_num = self.get_page_num(j)
                if page_num:
                    self.parse_html(j,page_num)
                else:
                    continue
    def parse_html(self,url,page_num):
        for step in range(1,int(page_num)+1):
            link_url = url+'pg{}/'.format(step)
            # 可以设置爬取的速度，爬太快的话可能被封，只有使用代理ip了
            time.sleep(1)
            print(link_url)
            try:
                response = requests.get(link_url,headers=self.headers)
            except Exception as e:
                pass
            response.encoding = response.apparent_encoding
            sel = parsel.Selector(response.text)
            #保存为csv格式，路径设置
            fp = open('lianjia1.csv', 'a', encoding='utf-8', newline='')
            for li in sel.xpath('//ul[@class="sellListContent"]/li'):
                title = li.xpath('.//div[@class="title"]/a[@data-el="ershoufang"]/text()').get()
                if title:
                    price = li.xpath('.//div[@class="totalPrice"]/span/text()').get()+li.xpath('.//div[@class="totalPrice"]/text()').get() if li.xpath('.//div[@class="totalPrice"]/span/text()') else ''
                    info = ''.join(li.xpath('.//div[@class="houseInfo"]/text()').get()).replace(' ','')
                    floor = li.xpath('.//div[@class="flood"]/div[@class="positionInfo"]//a//text()').getall()
                    if floor:
                        if len(floor)==2:
                            floor = '-'.join(floor).replace(' ','')
                        else:
                            floor = floor[0]
                    else:
                        floor=''
                    utilprice = re.sub('单价','',li.xpath('.//div[@class="unitPrice"]/span/text()').get())
                    followinfo = li.xpath('.//div[@class="followInfo"]/text()').get().split('/')[0].strip() if li.xpath('.//div[@class="followInfo"]/text()') else ''
                    vr = li.xpath('.//span[@class="vr"]/text()').get()
                    taxfree = li.xpath('.//div[@class="tag"]/span[@class="taxfree"]/text()').get() if li.xpath('.//div[@class="tag"]/span[@class="taxfree"]/text()') else ''
                    subway = li.xpath('.//div[@class="tag"]/span[@class="subway"]/text()').get() if li.xpath('.//div[@class="tag"]/span[@class="subway"]/text()') else ''
                    haskey = li.xpath('.//div[@class="tag"]/span[@class="haskey"]/text()').get() if li.xpath('.//div[@class="tag"]/span[@class="haskey"]/text()') else ''

                    print((title,price,info,floor,utilprice,followinfo,vr,taxfree,subway,haskey))
                    #保存为csv格式
                    writer = csv.writer(fp)
                    writer.writerow(list((title,price,info,floor,utilprice,followinfo,vr,taxfree,subway,haskey)))
                else:
                    continue
            fp.close()

if __name__ == '__main__':
    lianjia = Lianjia()
    lianjia.get_link_page_num()
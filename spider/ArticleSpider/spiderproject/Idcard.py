#!usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import parsel
from fake_useragent import FakeUserAgent
class IdCard():
    def __init__(self):
        self.start_url = 'http://sfzdq.uzuzuz.com/'
        self.headers = {
            'User-Agent':FakeUserAgent().random
        }
        self.f = open('./id_card.txt', 'a',encoding='utf-8')
        self.idcard_set = set()
    def parse_html(self,url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code==200:
                response.encoding = response.apparent_encoding
                return response.text
            else:
                return
        except Exception as e:
            print(e)

    def get_link(self):
        sel = parsel.Selector(self.parse_html(self.start_url))
        for li in sel.xpath('//ul[@class="list-group"]/li'):
            link = li.xpath('./a/@href').get()
            self.parse_card(link)
    def parse_card(self,link):
        sel = parsel.Selector(self.parse_html(link))
        for tr in sel.xpath('//table[@class="table"][2]//tr'):
            info = ','.join(tr.xpath('./td[position()<5]//text()').getall())
            position = ','+''.join([temp.strip() for temp in tr.xpath('./td[5]//text()').getall()])
            card_info = info+position
            print(card_info)
            self.f.write(card_info+'\n')
if __name__ == '__main__':
    id_card = IdCard()
    id_card.get_link()
    id_card.f.close()
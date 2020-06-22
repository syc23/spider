#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests,parsel,re
import csv
from gevent import monkey
monkey.patch_all()
from gevent.queue import Queue
import gevent,time
link = Queue()
class Ershoucar():
    def __init__(self):
        self.headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'uuid=143dde93-f3b5-4b10-e049-02345c53f088; antipas=6R875OAf52886Q9779IpmD; cityDomain=bj; user_city_id=12; ganji_uuid=9269680538801995813368; lg=1; clueSourceCode=10103000312%2300; sessionid=18fef3eb-d907-42cc-d31a-2ed1b2240349; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A41389621845%7D; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22ca_i%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22143dde93-f3b5-4b10-e049-02345c53f088%22%2C%22sessionid%22%3A%2218fef3eb-d907-42cc-d31a-2ed1b2240349%22%7D; preTime=%7B%22last%22%3A1564805268%2C%22this%22%3A1564759076%2C%22pre%22%3A1564759076%7D',
        }
    def parse_content(self,url):
        # while not link.empty():
        #     url = link.get_nowait()
        #     print(url)
            response = requests.get(url,headers=self.headers)
            response.encoding = response.apparent_encoding
            sel = parsel.Selector(response.text)
            for li in sel.xpath('//ul[contains(@class,"carlist")]/li'):
                title = li.xpath('.//h2[@class="t"]/text()').get()
                year= li.xpath('.//div[@class="t-i"]/text()[1]').get()
                if year:
                    year = re.match(r'(.*?)年',year).group(1) if re.match(r'(.*?)年',year) else ''
                    mile = li.xpath('.//div[@class="t-i"]/text()[2]').get()
                else:
                    continue
                if mile:
                    mile = re.match(r'(.*?)万公里', mile).group(1) if re.match(r'(.*?)万公里', mile) else ''
                    price = li.xpath('.//div[@class="t-price"]/p/text()').get()
                else:
                    continue
                print(title,year,mile,price)
                self.save_data([title,year,mile,price])
    def save_data(self,data=[]):
        with open('ershoucar.csv','a',encoding='utf-8',newline='') as f:
              writer = csv.writer(f)
              writer.writerow(data)
        pass
    def run(self):
        urls = list(map(lambda x:'https://www.guazi.com/bj/benz/o{}/'.format(x),[i for i in range(1,33)]))
        for url in urls:
            link.put_nowait(url)
            self.parse_content(url)
        # tasks_list = [gevent.spawn(self.parse_content) for i in range(5)]
        # gevent.joinall(tasks_list)
if __name__ == '__main__':
    ershoucar = Ershoucar()
    ershoucar.run()

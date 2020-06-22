#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import parsel
import random
def get_content(url):
    agent = [
        '27.203.140.233:8060',
        '47.106.140.89:8080',
        '149.129.106.176:8080'
    ]
    agents = random.choice(agent)
    print(agents)
    proxys = {
        'http':agents,
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
    content = requests.get(url,headers=headers,proxies=proxys).content.decode('utf-8')
    rel = parsel.Selector(content)
    # ip = rel.re(r'<td data-title="IP">(.*?)</td>')
    ip = rel.xpath('//td[@data-title="IP"]/text()').extract()
    print(ip)
    # print(rel)

if __name__ == '__main__':
    url = 'https://www.kuaidaili.com/free/'
    get_content(url)
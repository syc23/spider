#!usr/bin/env python  
#-*- coding:utf-8 -*-
import execjs
import time
import requests
import json
from fake_useragent import FakeUserAgent
class Ip(object):
    def __init__(self):
        self.headers = {
            'User-Agent':FakeUserAgent().random,
            'Cookie': 'sessionid=wmfzo33t3c8516eg4803roh9tsxp0zzf'
        }
    def deal_ip(self,data):
        js_obj = execjs.compile(open('零度代理.js','r',encoding='utf-8').read())
        return js_obj.call('decode_str',data)
    def token(self,page,num):
        js_obj = execjs.compile(open('token.js', 'r', encoding='utf-8').read())
        return js_obj.call('get_token', page,num)
    def deal_html(self):
        url = 'https://nyloner.cn/proxy?page={}&num={}&token={}&t={}'\
            .format(1,15,self.token(1,15),int(time.time()))
        response = requests.get(url,headers=self.headers)
        return response.json()
    def save_data(self):
        data = self.deal_html().get('list')
        true_data = self.deal_ip(data)
        true_data = json.loads(true_data)
        for i in true_data:
            ip_port = i['ip']+':'+i['port']
            print(ip_port)


if __name__ == '__main__':
    ip = Ip()
    ip.save_data()
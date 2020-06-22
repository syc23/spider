#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
import json,jsonpath
import re,time
import csv
import random
class Bili():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.baseurl= 'https://api.bilibili.com/x/space/acc/info?mid={}'
        self.f = open('bl_info.csv','a',newline='',encoding='utf-8')
    def get_info(self,mid):
        response = requests.get(self.baseurl.format(mid),headers=self.headers)
        time.sleep(0.5)
        response.encoding = response.apparent_encoding
        html = json.loads(response.text)
        if html:
            name = jsonpath.jsonpath(html,'$..name')[0] if jsonpath.jsonpath(html,'$..name') else ''
            birthday = jsonpath.jsonpath(html,'$..birthday')[0] if jsonpath.jsonpath(html,'$..birthday') else ''
            jointime = jsonpath.jsonpath(html,'$..jointime')[0] if jsonpath.jsonpath(html,'$..jointime') else ''
            coins = jsonpath.jsonpath(html,'$..coins')[0] if jsonpath.jsonpath(html,'$..coins') else ''
            level = jsonpath.jsonpath(html,'$..level')[0] if jsonpath.jsonpath(html,'$..level') else ''
            sex = jsonpath.jsonpath(html,'$..sex')[0] if jsonpath.jsonpath(html,'$..sex') else ''
            mid = jsonpath.jsonpath(html,'$..mid')[0] if jsonpath.jsonpath(html,'$..mid') else ''
            sign = jsonpath.jsonpath(html,'$..sign')[0] if jsonpath.jsonpath(html,'$..sign') else ''
            status = jsonpath.jsonpath(html,'$..status')[0] if jsonpath.jsonpath(html,'$..status') else ''
            rank = jsonpath.jsonpath(html, '$..rank')[0] if jsonpath.jsonpath(html,'$..rank') else ''
            with open('bl_info.csv','a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([birthday,jointime,coins,level,rank,mid,status,sex,sign,name])
            print(birthday,jointime,coins,level,rank,mid,sex,status,sign,name)
            print('*'*40)
        else:
            pass
    def get_follering_id(self,mid):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Referer': 'https://space.bilibili.com/{}/fans/fans'.format(mid),
        }
        url = 'https://api.bilibili.com/x/relation/followings?vmid={}&pn=1&ps=20&order=desc'.format(mid)
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        html = response.text
        if html:
            mid_list = re.findall(r'"mid":(\d+)', html)
            if mid_list is not None:
            # for mid in mid_list:
                self.get_follower_id(random.choice(mid_list))
    def get_follower_id(self,mid):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Referer': 'https://space.bilibili.com/{}/fans/fans'.format(mid),
        }
        url = 'https://api.bilibili.com/x/relation/followers?vmid={}&pn=1&ps=20&order=desc'.format(mid)
        response = requests.get(url,headers=headers)
        response.encoding = response.apparent_encoding
        html = response.text
        if html:
            mid_list =re.findall(r'"mid":(\d+)',html)
            if mid_list is not None:
                for s_mid in mid_list:
                    self.get_info(s_mid)
                self.get_follering_id(random.choice(mid_list))
if __name__ == '__main__':
    bl = Bili()
    bl.get_follering_id('38520275')
#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import jsonpath,json
import time,pprint
import csv
class Maoyan():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Referer': 'http://m.maoyan.com/movie/1211270/comments?_v_=yes',
            'X-Requested-With': 'superagent'
        }
        self.proxy = {
             'http':'101.231.104.82:80'
        }
        self.base_url = 'http://m.maoyan.com/review/v2/comments.json'
    def get_content(self,param):
        time.sleep(0.5)
        response = requests.get(self.base_url,params=param,headers = self.headers,proxies = self.proxy)
        print(response.url)
        json_str = response.content.decode()
        json_data = json.loads(json_str)
        contents_ = jsonpath.jsonpath(json_data,'$..content')
        genders = jsonpath.jsonpath(json_data,'$..gender')
        scores = jsonpath.jsonpath(json_data,'$..score')
        comments = jsonpath.jsonpath(json_data,'$..0.name')
        nicks = jsonpath.jsonpath(json_data,'$..nick')
        for content_,gender,score,comment,nick in zip(contents_,genders,scores,comments,nicks):
            data_list = [nick,gender,score,comment,content_]
            self.save_data(data_list)
            # break
    def save_data(self,data):
        with open('./maoyan1.csv','a',newline='',encoding='utf-8') as f:
             writer = csv.writer(f)
             writer.writerow(data)
    def run(self):
        params = [{
            'movieId': '1211270',
            'userId': '-1',
            'offset': offset,
            'limit': '15',
            # 'ts': int(time.time()*1000),
            'type': '3'
        } for offset in range(15,500000,15)]
        for param in params:
            self.get_content(param)
            # break
            # break
if __name__ == '__main__':
    maoy = Maoyan()
    maoy.run()

#!usr/bin/env python  
#-*- coding:utf-8 -*-
import jsonpath
import requests
import json
import random
import pandas as pd
import re
import csv
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
# def get_sing_mid():
#     data = pd.read_csv(r'./singer_to_mid.csv')
#     for name,midd in zip(data['name'],data['midd']):
#         print('正在下载{}歌单中的mid'.format(name))
#         url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
#         param_data = {"comm":{"ct":24,"cv":0},"singer":{"method":"get_singer_detail_info","param":{"sort":5,"singermid":midd,"sin":0,"num":200},"module":"music.web_singer_info_svr"}}
#         params = {
#             'data':json.dumps(param_data).replace(' ','')
#         }
#         response = requests.get(url,headers=headers,params=params).json()
#         f = open('./sing_mid.csv','a',newline='',encoding='utf-8')
#         for index in range(len(response['singer']['data']['songlist'])):
#             title = response['singer']['data']['songlist'][index]['title']
#             mid = response['singer']['data']['songlist'][index]['mid']
#             if title and mid:
#                 writer = csv.writer(f)
#                 writer.writerow([title,mid])
# get_sing_mid()






# singer_to_mid = []

def get_singer():
    proxy = {
        'http': '118.24.246.249:80'
    }
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    params_list = [{'singerList': {'module': 'Music.SingerListServer', 'method': 'get_singer_list',
                     'param': {'area': -100, 'sex': -100, 'genre': -100, 'index': -100, 'sin': (page-1)*80, 'cur_page': page}}}
     for page in range(1,299)]
    f = open(r'./singer_to_mid.csv','a',encoding='utf-8',newline='')
    for index,param in enumerate(params_list):
        ucgi = ('getUCGI' + (str(random.random()).replace('0.', '')))
        params = {
            '_': ucgi,
            'g_tk': '5381',
            'data': json.dumps(param).replace(' ','')
        }
        print('第{}页数据处理完毕'.format(index))
        print(params)
        response = requests.get(url,headers=headers,params=params,proxies=proxy).json()
        singer_names = jsonpath.jsonpath(response,'$..singer_name')
        singer_mids = jsonpath.jsonpath(response, '$..singer_mid')
        try:
            for name,mid in zip(singer_names,singer_mids):
                # singer_to_mid.append({name:mid})
                if name and mid:
                    writer = csv.writer(f)
                    writer.writerow([name,mid])
        except:
            continue
    f.close()
get_singer()


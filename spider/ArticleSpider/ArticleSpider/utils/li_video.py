#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import re,os
import random
from urllib import request
from multiprocessing import pool
def get_content(url):
    agent = [
        '27.203.140.233:8060',
        '47.106.140.89:8080',
        '149.129.106.176:8080'
    ]
    agents = random.choice(agent)
    proxys = {
        'http':agents,
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
    content = requests.get(url,headers=headers,proxies=proxys).content.decode('utf-8')
    ids = re.findall(r'<div class="vervideo-bd">.*?<a href="(.*?_.*?)" class="vervideo-lilink actplay">',content,re.S)
    title_list = re.findall(r'<div class="vervideo-title">(.*?)</div>',content,re.S)
    titles = list(map(lambda x:re.sub(r'？|！|\?|,|，|!|：|','',x),title_list))
    return ids,titles
def get_info(url):
    ids,titles = get_content(url)
    for id ,title in zip(ids,titles):
        down_video(id,title)
def down_video(id,title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
    base_url = 'https://www.pearvideo.com/'
    down_detaile_url = base_url+id
    content = requests.get(down_detaile_url,headers=headers).content.decode('utf-8')
    down_url = re.findall(r'srcUrl="(.*?)"',content,re.S)
    if down_url:
        file_name = os.path.join('video',title+'.mp4')
        down_url = down_url[0]
        print(title,'正在下载')
        request.urlretrieve(down_url,file_name)
        print(title,'下载完成')
    else:
        return
if __name__ == '__main__':
    urls = list(
        map(lambda x: 'https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=31&start={}'.format(x),[i for i in range(0, 500, 12)]))
    p = pool.Pool(6)
    p.map(get_info,urls)
    # get_info()
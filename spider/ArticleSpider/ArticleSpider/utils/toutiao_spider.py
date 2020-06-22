#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import time
import os
import urllib
from urllib import parse,request
import re
def get_url(offset,keyword):
    url = 'https://www.toutiao.com/api/search/content/'
    keyw = parse.quote(keyword)
    headers = {
        'path': '/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword={}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp={}'.format(offset,keyw,int(time.time()*1000)),
        'authority': 'www.toutiao.com',
        'cookie': 'uuid="w:a60111c8434d420b9a7ccd89f21e12a7"; tt_webid=6713910078958913028; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6713910078958913028; __tasessionId=vp0jrqr5v1563204025453; csrftoken=5ad71420093dea7c9b6a3b64dc1921ad; s_v_web_id=89872cf3f1feb2854ae196027f1e635d',
        'referer': 'https://www.toutiao.com/search/?keyword={}'.format(keyw),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time()*1000)
    }
    try:
        html = requests.get(url=url,headers=headers,params=params,timeout=3).json()
    except Exception as e:
        print(e)
    data = html['data']
    for i in range(len(data)):
        if 'item_id' and 'title' in data[i].keys():
            title = data[i]['title']
            id = data[i].get('item_id')
            parse_detail(title,id)
def parse_detail(title,id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    detail_url = 'https://www.toutiao.com/a{}/'.format(id)
    try:
        html = requests.get(detail_url,headers=headers,timeout=3).content.decode('utf-8')
    except Exception as e:
        print(e)

    info = re.findall(r'http:\\.*?\\.*?\.pstatp\.com\\.*?\\.*?-image\\u002F(.*?)\\&quot;\simg_width.*?',html,re.S)
    img_url_list = list(map(lambda x:'http://p3.pstatp.com/large/pgc-image/{}'.format(x),info))
    file_path = 'imgs/'+title
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    for img_url in img_url_list:
        print(title,img_url)
        request.urlretrieve(img_url,file_path+'/'+re.split('/',img_url)[-1]+'.jpg')

if __name__ == '__main__':
    get_url(0,'街拍')
    # parse_detail('https://www.toutiao.com/a6712602886531973645/')
#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
import re,os
from urllib import request
def get_id():
    url = 'http://www.yy8844.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    html = requests.get(url,headers=headers).content.decode('gb18030')
    id = re.findall(r'<input type="checkbox" name="id" value=".*?\|.*?\|.*?\|(\d+)\|.*?\|.*?\|.*?">',html,re.S)
    names = re.findall(r"<a href=.*? target='.*?'>(.*?)</a> ",html,re.S)
    for music_id,name in zip(id,names):
        down_music(music_id,name)
        break
def down_music(music_id,name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    music_url = 'http://65.ierge.cn/{}/{}/{}.mp3?v=0524'.format(int(int(music_id)/30000),int(int(music_id)/2000),music_id)
    file_name = os.path.join('music',name+'.mp3')
    print("正在下载:",name)
    request.urlretrieve(music_url,file_name)
    print(name,"下载完成")



if __name__ == '__main__':
    # down_music(id)
    get_id()
#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import os
import re
from multiprocessing import pool
class Wyy(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
        }
        self.base = 'https://music.163.com'
    def deal_str(self,name):
        name = re.sub(r'の|み|\s|з|\||°|-|◕|な|お|】|【|✞|✞|い|·|\.|「|」|な|!|o|）|（|か|ぜ|❀|は|が|く|れ|\|/|ས|ྒ|ྱ|ེ|་|ན|ང|་|ས|ྙ|ུ|ང|་|བ|ུ|།|丨|\(|\)|ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ|：|"|"|｜','',name)
        return name
    def get_link(self,url):
        try:
            response = requests.get(url,headers=self.headers)
            response.encoding = response.apparent_encoding
            title_links = re.findall(r'<p class="dec">.*?<a title="(.*?)" href="(.*?)" class=".*?">.*?</a>',response.text,re.S)
            for title,link in title_links:
                link = self.base+link
                try:
                    self.get_id(title,link)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    def get_id(self,title,link):
        print(link)
        response = requests.get(link,headers=self.headers)
        response.encoding = response.apparent_encoding
        ids = re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>',response.text,re.S)
        for id,name in ids:
            pass
            # try:
            #     self.down_music(id,name,title)
            # except Exception as e:
            #     print(e, '歌曲：', name + '下载失败！')
    def down_music(self,id,name,title):
        title = self.deal_str(title)
        if title:
            file_dir = os.path.join(r'D:\wangyiyun',title)
        else:
            file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), id)
        name = self.deal_str(name)
        if name:
            file_name = os.path.join(file_dir,name+'.m4a')
        else:
            file_name = os.path.join(file_dir, id+ '.m4a')
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
            print('创建歌单:', file_dir)
        down_url = 'https://link.hhtjim.com/163/{}.mp3'.format(id)
        response = requests.get(down_url,headers = self.headers)
        print('歌曲', name, '正在下载')
        with open(file_name, 'wb') as fp:
            fp.write(response.content)
        print('歌曲', name, '下载完成')
if __name__ == '__main__':
    wy = Wyy()
    urls = list(map(lambda x:'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'.format(x),[i for i in range(0,1296,35)]))
    p = pool.Pool(6)
    p.map(wy.get_link,urls)
    p.close()
    p.join()

    1336856865
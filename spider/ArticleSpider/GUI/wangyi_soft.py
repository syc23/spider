#!usr/bin/env python  
#-*- coding:utf-8 -*-
import tkinter
import os
import json
import pandas as pd
import requests
from tkinter import scrolledtext
from tkinter import END
class Wangyi_Soft():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.proxys = {
            'http':'118.24.246.249:80'
        }
        self.root = tkinter.Tk()
        self.root.minsize(600,600)
        self.root.title('QQ音乐下载器1.0')
        self.windows()
        self.root.mainloop()
    # 界面布局
    def windows(self):
        # 提示显示
        self.label_disply = tkinter.Label(self.root, text='请输入歌手:')
        self.label_disply.place(x=8, y=16, width=80, height=30)
        # 输入框
        self.entry = tkinter.Entry(self.root)
        self.entry.place(x=90, y=16, width=400, height=30)
        # 下载按钮
        self.download_btn = tkinter.Button(self.root, text='开始下载',command=self.get_sing_mid)
        self.download_btn.place(x=500, y=16, width=80, height=30)
        # 信息展示区域
        self.label_info = scrolledtext.ScrolledText(self.root, bg='white',font=20)
        self.label_info.place(x=10, y=51, width=580, height=543)
    def get_sing_mid(self):
        self.info = self.entry.get()
        data = pd.read_csv(r'./singer_to_mid.csv')
        flag = False
        for name, midd in zip(data['name'],data['midd']):
            if name == self.info:
                flag = True
                self.label_info.insert(END, '正在下载:' + '\n')
                url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
                param_data = {"comm": {"ct": 24, "cv": 0}, "singer": {"method": "get_singer_detail_info",
                                                                      "param": {"sort": 5, "singermid": midd, "sin": 0,
                                                                                "num": 200},
                                                                      "module": "music.web_singer_info_svr"}}
                params = {
                    'data': json.dumps(param_data).replace(' ', '')
                }
                response = requests.get(url, headers=self.headers, params=params).json()
                for index in range(len(response['singer']['data']['songlist'])):
                    title = response['singer']['data']['songlist'][index]['title']
                    mid = response['singer']['data']['songlist'][index]['mid']
                    path = os.path.join('music', name+'.mp3')
                    download_url = 'https://link.hhtjim.com/qq/{}.mp3'.format(mid)
                    with open(path,'wb') as f:
                        f.write(requests.get(download_url,headers=self.headers,proxies=self.proxys).content)
                    self.label_info.insert(END, str(index + 1) + ':' + title + '\n')
                break
        if flag==False:
            self.label_info.insert(END, '暂无该歌手的相关数据' + '\n')
wangyi_sotf = Wangyi_Soft()
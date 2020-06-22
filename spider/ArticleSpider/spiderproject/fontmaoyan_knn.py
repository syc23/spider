#!usr/bin/env python  
#-*- coding:utf-8 -*-
"""
    猫眼字体反爬(UNICODE不同，字形不同，坐标相似，采用knn求其坐标相似的字体)
"""
import requests
from fake_useragent import UserAgent
from fontTools.ttLib import TTFont
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
import parsel

from urllib import parse

# class Model():
#     def __init__(self):
#         self.unicode_value1 = {
#             "uniE374": "7",
#             "uniE7D3": "3",
#             "uniE8BE": "1",
#             "uniEB84": "4",
#             "uniECB6": "5",
#             "uniEF4C": "8",
#             "uniF285": "2",
#             "uniF310": "0",
#             "uniF40C": "9",
#             "uniF754":"6"
#         }
#         self.unicode_value2={
#             "uniE034": "3",
#             "uniE267": "7",
#             "uniE578": "8",
#             "uniE587": "0",
#             "uniE6F5": "1",
#             "uniEDD9": "2",
#             "uniF157": "5",
#             "uniF1D2": "9",
#             "uniF2EC": "4",
#             "uniF7E7":"6"
#         }
#         self.unicode_value3 ={
#             "uniE2AD": "8",
#             "uniE632": "0",
#             "uniE835": "2",
#             "uniE875": "4",
#             "uniEAB9": "3",
#             "uniECAC": "9",
#             "uniEEAB": "7",
#             "uniF52A": "6",
#             "uniF5CC": "5",
#             "uniF8A5": "1",
#         }
#         self.unicode_value4 = {
#             "uniE436": "9",
#             "uniE56D": "5",
#             "uniE5D5": "2",
#             "uniE608": "0",
#             "uniE75B": "3",
#             "uniEB5C": "7",
#             "uniF2E5": "4",
#             "uniF3E1": "8",
#             "uniF582": "6",
#             "uniF7EF":"1"
#         }
#         self.unicode_value5 = {
#             "uniE0A0": "9",
#             "uniE326": "5",
#             "uniE3E0": "7",
#             "uniE8FE": "6",
#             "uniEB9E": "0",
#             "uniEC8D": "4",
#             "uniED28": "8",
#             "uniEF14": "1",
#             "uniF20C": "2",
#             "uniF2FA":"3"
#         }
#         self.unicode_value6 = {
#             "uniE31F": "1",
#             "uniE38C": "8",
#             "uniE956": "2",
#             "uniED05": "5",
#             "uniED31": "9",
#             "uniEE75": "0",
#             "uniEFA5": "7",
#             "uniF207": "3",
#             "uniF2AB": "6",
#             "uniF8DD":"4"
#         }
#         self.unicode_value7 = {
#             "uniE291": "0",
#             "uniE785": "7",
#             "uniE834": "2",
#             "uniED2F": "4",
#             "uniEE19": "3",
#             "uniEEEE": "8",
#             "uniEF66": "9",
#             "uniF0FC": "5",
#             "uniF5FB": "1",
#             "uniF7D7": "6"
#         }
#         self.model = KNeighborsClassifier(n_neighbors=1)
#     def transform(self):
#         x, y = [], []
#         file_list = ['./font/1.woff','./font/2.woff','./font/3.woff','./font/4.woff','./font/5.woff','./font/6.woff','./font/7.woff']
#         unicode_list = [self.unicode_value1,self.unicode_value2,self.unicode_value3,self.unicode_value4,self.unicode_value5,self.unicode_value6,self.unicode_value7]
#         for g,unicode_value in zip(file_list,unicode_list):
#             maoyan = TTFont(g)
#             for i in maoyan.getGlyphNames()[1:-1]:
#                 temp = np.zeros(shape=(150,))
#                 tmp = list(maoyan['glyf'][i].coordinates)
#                 tmp = [list(i) for i in tmp]
#                 tmp = [j for i in tmp for j in i]
#                 for k in range(len(tmp)):
#                     temp[k] = tmp[k]
#                 x.append(temp)
#                 y.append(unicode_value[i])
#
#         x = np.array(x)
#         y = np.array(y)
#         return x,y
#     def train(self):
#         print('正在训练模型！')
#         x,y = self.transform()
#         self.model.fit(x,y)
#         s = pickle.dumps(self.model)
#         f = open('./model/knn.ckpt','wb')
#         f.write(s)
#         f.close()
#         print('训练结束！')
#
class AntiFont():
    def __init__(self):
        pass

    def get_coor_unicode(self,file_id):
        """
        获取字体文件的坐标和unicode:'uniECB6'
        :return:
        """
        fontpath = './font/{}.woff'.format(file_id)
        print(fontpath)
        maoyan = TTFont(fontpath)
        coor_list,unicode_list = [],[]
        for i in maoyan.getGlyphNames()[1:-1]:
            temp = np.zeros(shape=(150,))
            tmp = list(maoyan['glyf'][i].coordinates)
            tmp = [j for i in tmp for j in i]
            for k in range(len(tmp)):
                temp[k] = tmp[k]
            coor_list.append(temp)
            unicode_list.append(i)

        coor_list = np.array(coor_list)

        return coor_list,unicode_list

    def transform(self,woffid):
        """
        将获取坐标，用KNN算法将坐标转化为相似的数字，然后将unicode和获取的数字转化为字典
        {'uniF285': '2'}，{'uniF310': '0'}
        :param coordinates:
        :param digit:
        :return:
        """
        coordinates, digit = self.get_coor_unicode(woffid)
        # 加载模型预测
        f = open('./model/knn.ckpt', 'rb')
        s = f.read()
        knn_model = pickle.loads(s)
        pred = knn_model.predict(coordinates)
        unicodetovalue = dict(zip(digit, pred))
        f.close()
        return unicodetovalue
class Maoyan():
    def __init__(self):
        self.headers = {
            'Host': 'maoyan.com',
            'Referer': 'https://maoyan.com/films',
            'User-Agent':UserAgent().random
        }

        self.url = 'https://maoyan.com/films?showType=3&offset=30'

    def getcontent(self,url):
        response = requests.get(url,headers=self.headers,proxies={'http':'http://47.96.129.64'})
        response.encoding=response.apparent_encoding

        content = response.text
        return parsel.Selector(content)
    def get_content(self,url):
        response = requests.get(url,headers=self.headers,proxies={'http':'http://47.96.129.64'})
        response.encoding=response.apparent_encoding

        content = response.text
        return content
    def get_detail(self):
        sel = self.getcontent(self.url)
        antifont = AntiFont() # 字体反爬
        for i in sel.xpath('//dl[@class="movie-list"]//dd'):
            link = i.xpath('./div[position()=1]/a/@href').get()
            link = parse.urljoin('https://maoyan.com/',link)
            detail_content = self.get_content(link)
            se = parsel.Selector(detail_content)
            woffurl = se.re("url\('//vfile.meituan.net/colorstone/(.*?).woff'\) format\('woff'\);")
            if woffurl and len(woffurl)==1:
                print(link)
                woffid = woffurl[0]
                wl = 'https://vfile.meituan.net/colorstone/{}.woff'.format(woffid)
                with open('./font/{}.woff'.format(woffid),'wb') as f:
                    f.write(requests.get(wl).content)
                unicodetovalue = antifont.transform(woffid)
                for key,value in unicodetovalue.items():
                    key = key.lower().replace('uni','&#x') + ';'
                    detail_content = detail_content.replace(key,value)
                see = parsel.Selector(detail_content)
                item1 = see.xpath("")
                item2 = see.xpath("")
                item3 = see.xpath("")
                item4 = see.xpath("")
                print(item1,item2,item3,item4)
            break
if __name__ == '__main__':
    manyan = Maoyan()
    manyan.get_detail()


# if __name__ == '__main__':
#
#     # 模型训练
#     # model = Model()
#     # model.train()
#
#     # 模型预测
#     antifont = AntiFont()
#     print(antifont.transform())



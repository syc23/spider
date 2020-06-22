# #!usr/bin/env python
# #-*- coding:utf-8 -*-
# import re
# import os
# import sys
# # base = os.path.dirname(os.path.abspath(__file__))
# # IMAGES_STORE= os.path.join(base,'images')
# # print(IMAGES_STORE)
# a = '网友：zw985 发言时间：2019-07-07 12:21:45'
# b = '网友：莎如雪 发言时间：2019-07-05 11:18:40'
# c = '网友：潢涌仔 发言时间：2007-11-12 08:28:21  受理时间：2008-08-28 17:21:11'
# d = '网友：牛波 发言时间：2007-09-25 00:46:20  受理时间：2008-09-16 17:24:47'
# import re
# e = ' 提问：关于二手房交易个税问题  编号:198645'
# # print(re.match(reg,b).group(2))
#
# # f = '  网友：小龙在世 发言时间：2018-10-12 10:14:05  '
# # reg  = r'.*：(.*?) .*：(.*?)  '
# # print(re.findall(reg,f))
# import datetime
#
# import time
# # a = 1562648322253
# # print(round(time.time()*1000))
# # print(int(time.time()*1000))
#
# import redis
# import MySQLdb
# import json
#
# def process_item():
#     #连接mysql数据库
#     mysql_cli = MySQLdb.connect(host='localhost',port=3306,user='root',passwd = '147258369',db='spider',charset='utf8')
#     # 创建mysql操作游标对象，执行mysql语句
#     cursor = mysql_cli.cursor()
#     # 将数据从redis数据库中pop出来
#     cursor = mysql_cli.cursor()
#     sql = 'insert into test(name) values(["中国","小日本"])'
#     mysql_cli.commit()
#     # 提交事务
#     mysql_cli.commit()
#     # 关闭游标
#     cursor.close()
# if __name__ == '__main__':
#     process_item()
# from urllib import parse
#
# print(parse.quote("街拍"))

# print(list(map(lambda x:x+1,[1,2,3,4])))
import requests
proxys = {
    # 'http':'163.204.246.42:9999',
    # 'http': '113.128.27.126:9999',
    # 'http':'109.200.187.208:8080',
    # 'http': '182.35.84.183:9999',
    'http':'110.243.20.31:9999'

}
headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
     }
html = requests.get('http://httpbin.org/get',headers=headers,proxies=proxys).content.decode('utf-8')
print(html)
# res = requests.get('http://httpbin.org/get',headers=headers,proxies=proxys)
# 万能编码
# res.encoding = res.apparent_encoding
# print(res.text)
# import parsel
# sel = parsel.Selector()
# sel.re()

# data = 'WEATHER_COOKIE_CITY_KEY=101040100%7C%E9%87%8D%E5%BA%86; baidu_shuffle_0309_3=1; baidu_shuffle_0309=1; baidu_shuffle_20180821=1; _dbsg=ij7t5mdfksda8fksdafka19b04cef36a; CNZZDATA30089211=cnzz_eid%3D1487965383-1556769160-http%253A%252F%252Fnews.duba.com%252F%26ntime%3D1556769160; UM_distinctid=16b0c3ca2a56-02ecbbcb2160a6-2b6f686a-1fa400-16b0c3ca2a6960; changevertips=1; t_manual=0; t_web_page=1; kws_dubasvrid=1d39d7ca20c19b9f5a16cde7000bda60; orpv=1; redLinkIdxs=1%2C5%2C1%2C5%2C1%2C6%2C1%2C6%2C2%2C5%2C1%2C4%2C2%2C5%2C1%2C5%2C1%2C5%2C2%2C4; userIDF=15636734022354e63j; CNZZDATA30069637=cnzz_eid%3D477995153-1563672919-%26ntime%3D1563716119; __kp=4upppnimecrvy4seq754xcbi9vix; __kt=1563673413; act=7/21:2; __vgl=1; reqtimesN=NaN; ggRuleIndex=0; leftHookTipIndex=4; Hm_lvt_47c19b16e7362939c0067988e0da87cd=1563534956,1563673408; Hm_lpvt_47c19b16e7362939c0067988e0da87cd=1563721016'
# data_dic = {x.split('=')[0]:x.split('=')[1] for x in data.split('; ')}
# print(data_dic)
# # print(data.split('; '))
# a = 'http://www.4567kan.com/index.php/vod/show/id/1/page/2.html'
# import hashlib
# source = '我醉过三次酒，后来我直接戒酒了！第一次，同学聚会，我喝醉了之后去上卫生间，错进了女生的卫生间，还在里面睡着了，要不是女生的惊叫，同学们硬是把我从里面拖出来，我可以在里面睡到天亮！第二次，我喝醉之后，在小区的石头大象上面跳起了印度阿三的新娘嫁人新郎不是我！问题是，我是脱光光跳的！……第三次，在家喝的酒，然后在卫生间和镜子，石头，剪刀，布。二十分钟内各有胜负！……'
#
# m = hashlib.sha256(source.encode()).hexdigest()
# print(m)
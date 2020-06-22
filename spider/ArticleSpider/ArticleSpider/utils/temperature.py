#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
from lxml import etree
from matplotlib import pyplot as plt

from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

all_data = []
def spider(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    html = requests.get(url,headers=headers).content.decode("utf-8")
    text = etree.HTML(html)
    div_list = text.xpath('//div[@class="conMidtab"]')[0]
    div2_list = div_list.xpath('./div[@class="conMidtab2"]')
    for i in div2_list:
        tr_list = i.xpath(".//tr")[2:]
        for index,tr in enumerate(tr_list):
            city = tr.xpath("./td[1]/a/text()")[0]
            if index==0:
                low_temp = tr.xpath("./td[5]/text()")[0]
            else:
                low_temp = tr.xpath("./td[4]/text()")[0]
            all_data.append({'city':city,'low_temp':int(low_temp)})

def main():
    url_list = [
     'http://www.weather.com.cn/textFC/hb.shtml',
    'http://www.weather.com.cn/textFC/db.shtml',
    'http://www.weather.com.cn/textFC/hd.shtml',
    'http://www.weather.com.cn/textFC/hz.shtml',
     'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
]
    for url in url_list:
        spider(url)
if __name__ == '__main__':
    main()
    print(all_data)
    all_data.sort(key=lambda data: data['low_temp'], reverse=True)
    data = all_data[0:10]
    print(data)
    citys = []
    min_temp = []
    for i in data:
        citys.append(i['city'])
        min_temp.append(i['low_temp'])
    plt.bar(citys, min_temp)
    plt.show()
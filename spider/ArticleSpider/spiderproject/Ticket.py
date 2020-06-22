#!usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import parsel
def getdata():
    response = requests.get("https://datachart.500.com/ssq/history/newinc/history.php?limit=8000&sort=0")
    response.encoding = response.apparent_encoding
    # 把所有的html信息交给etree
    sel = parsel.Selector(response.text)
    trs = sel.xpath("//tbody[@id='tdata']/tr")
    for tr in trs:
        datas = tr.xpath('td/text()').getall()
        data = map(lambda x: x.replace(",", "").replace("\xa0", ""), datas)
        data = ','.join(data)
        print(data)
        break

import pandas as pd
import matplotlib.pyplot as plot

def data_analysis():
    df = pd.read_csv("data.csv", header=None)
    # 提取红球开奖号码
    red_ball = df.loc[:, 1:6]
    # 红球开奖号码出现的次数
    red_counts = pd.value_counts(red_ball.values.flatten())
    # 篮球
    blue_ball = df.loc[:, [7]]
    blue_counts = pd.value_counts(blue_ball.values.flatten())
    # 可视化
    plot.pie(red_counts, labels=red_counts.index, radius=1, wedgeprops={"width": 0.3})
    plot.pie(blue_counts, labels=blue_counts.index, radius=0.5, wedgeprops={"width": 0.3})
    plot.show()

if __name__ == '__main__':
    getdata()
    data_analysis()

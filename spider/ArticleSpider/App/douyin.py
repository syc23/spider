#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
import parsel
import re
from fake_useragent import FakeUserAgent
import urllib3
urllib3.disable_warnings()

headers = {
    'User-Agent' : FakeUserAgent().random,
}

def unicodetovalue(data):
    map_ = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
    ]
    for i in map_:
        for j in i['name']:
            data = re.sub(j,str(i['value']),data)
    return data

def get_detail():
    item = {}
    url = 'https://www.iesdouyin.com/share/user/51921356560'
    response = requests.get(url,headers=headers,verify=False)
    content = unicodetovalue(response.text)
    sel = parsel.Selector(content)
    nickname = sel.xpath('//p[@class="nickname"]/text()').get()
    item['nicename'] = nickname if nickname else ''
    job = sel.xpath('//span[@class="info"]/text()').get()
    item['job']= job if job else ''
    id_ = sel.xpath('//p[@class="shortid"]//text()').getall()
    if id_:
        item['id_'] = ''.join([i.strip() for i in id_]).replace('抖音ID：','')
    signature = sel.xpath('//p[@class="signature"]/text()').get()
    item['signature'] = signature if signature else ''
    focus = sel.xpath('//span[@class="focus block"]//text()').getall()
    if focus:
        item['focus'] = ''.join([i.strip() for i in focus]).replace('关注','')
    else:
        item['focus'] = ''
    follower = sel.xpath('//span[@class="follower block"]//text()').getall()
    if follower:
        item['follower'] = ''.join([i.strip() for i in follower]).replace('粉丝', '')
    else:
        item['follower'] = ''
    liked = sel.xpath('//span[@class="liked-num block"]//text()').getall()
    if liked:
        item['liked'] = ''.join([i.strip() for i in liked]).replace('赞', '')
    else:
        item['liked'] = ''
    user_work = sel.xpath('//div[@class="user-tab active tab get-list"]//text()').getall()
    if user_work:
        user_work = ''.join([i.strip() for i in user_work]).replace('作品','')
        item['user_work'] =user_work
    else:
        item['user_work'] = ''
    user_like = sel.xpath('//div[@class="like-tab tab get-list"]//text()').getall()
    if user_like:
        user_like = ''.join([i.strip() for i in user_like]).replace('喜欢','')
        item['user_like'] = user_like
    else:
        item['user_like'] = ''
    print(item)
get_detail()

#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import json
import random,time
from multiprocessing import pool
import pymongo
coun = 0
mongo_py = pymongo.MongoClient()
db = mongo_py['spider']
collection = db['jiaoyou1']
def get_content(url):
    agent = [
        '119.41.236.180:8010',
        '47.106.140.89:8080',
        '39.137.69.6:8080'
    ]
    agents = random.choice(agent)
    print(agents)
    proxys = {
        'http':agents,
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
    content = requests.get(url,headers=headers,proxies=proxys).json()
    time.sleep(0.5)
    return content
def get_info(url):
    print(url)
    item = {}
    if 'list' in get_content(url)['data'].keys():
        content = get_content(url)['data']['list']
        for i in range(len(content)):
            item['avatar'] = content[i]['avatar']
            item['birthdayyear'] = content[i]['birthdayyear']
            item['city'] = content[i]['city']
            item['education'] = content[i]['education']
            item['gender'] = content[i]['gender']
            item['height'] = content[i]['height']
            item['marry'] = content[i]['marry']
            item['monolog'] = content[i]['monolog']
            item['salary'] = content[i]['salary']
            item['province'] = content[i]['province']
            item['monologflag'] = content[i]['monologflag']
            item['_id'] = content[i]['userid']
            item['detail_url'] = 'http://www.7799520.com/user/{}.html'.format(item['_id'])
            item['username'] = content[i]['username']
        # item(avatar=avatar,birthdayyear=birthdayyear,city=city,education=education,gender=gender, \
        #      height=height,marry=marry,monolog=monolog,salary=salary,province=province, \
        #      monologflag=monologflag,userid=userid,detail_url=detail_url,username=username,)
        #     with open('jiaoyou.json','a',encoding='utf-8') as f:
        #         f.write(json.dumps(item,ensure_ascii=False)+'\n')
            save_data(item)
    else:
        global coun
        coun = coun+1
        get_content(url)
        print(coun)
def save_data(item):
    try:
        collection.insert(item)
    except Exception as e:
        print(e)
    finally:
        mongo_py.close()
if __name__ == '__main__':
    urls = list(map(lambda x: 'http://www.7799520.com/api/user/pc/list/search?gender=2&marry=1&education=50&page={}'.format(x),[i for i in range(1, 1500)]))
    # get_info()
    p = pool.Pool(6)
    p.map(get_info,urls)
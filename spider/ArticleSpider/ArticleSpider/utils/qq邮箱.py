#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import re
from multiprocessing import pool
def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # url = 'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=python%BD%CC%B3%CC%20%D3%CA%CF%E4&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn=1'
    html = requests.get(url,headers=headers).content.decode('gbk')
    detail_link = re.findall(r'<a data-tid="\d+" data-fid="\d+" class="bluelink" href="(.*?)" class="bluelink" target="_blank" >.*?</a>',html,re.S)
    for link in list(map(lambda x:'http://tieba.baidu.com'+x,detail_link)):
        get_qq_email(link)
def get_qq_email(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    html = requests.get(link).content.decode('utf-8')
    email = list(set(re.findall(r'[0-9]+@[a-zA-Z]+\.[a-z]+',html)))
    print(email)
    fp = open('email.txt','a')
    for qq in email:
        fp.write(qq+'\n')
    next_url = re.findall(r'<a href="(.*?)">下一页</a>',html)
    if next_url:
        get_qq_email('http://tieba.baidu.com'+next_url[0])
    else:
        print("最后一页爬取完成！")
        return
if __name__ == '__main__':
    url_list= list(map(lambda x:'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%CA%D3%C6%B5%20%D3%CA%CF%E4&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn={}'.format(x),[i for i in range(1,77)]))
    # for url in url_list:
    #     get_url(url)
    p = pool.Pool()
    p.map(get_url,url_list)

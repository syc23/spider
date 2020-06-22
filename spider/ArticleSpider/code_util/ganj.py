#!usr/bin/env python  
#-*- coding:utf-8 -*-
from fake_useragent import UserAgent
from code_util import ydm
import requests
import parsel

index_url = 'https://passport.ganji.com/login.php?next=/'
login_url = 'https://passport.ganji.com/login.php'
headers ={
        'User-Agent':UserAgent().random
    }
sess = requests.Session()
def parse():
    response = sess.get(index_url,headers=headers)
    response.encoding = response.apparent_encoding
    sel = parsel.Selector(response.text)
    __hash__ = sel.re(r'"__hash__":"(.*?)"')[0]
    # next = sel.xpath('//input[@name="next"]/@value').extract_first()
    # setcookies = sel.xpath('//input[@name="setcookie"]/@value').extract_first()
    # print(next,setcookies)
    login(__hash__)
def login(__hash__):
    with open('code.png','wb') as f:
        f.write(sess.get('https://passport.ganji.com/ajax.php?dir=captcha&module=login_captcha').content)

    code = ydm.code()
    data = {
        'username': '18883245172',
        'password': '147258369',
        'setcookie': 14,
        'checkCode':code,
         'next': '/',
        'source': 'passport',
        '__hash__': __hash__
    }
    cont = sess.post(login_url,data=data,headers=headers).text
    print(cont)
    with open('ganji_index.html', 'w', encoding='utf-8') as f:
        f.write(sess.get('http://www.ganji.com/vip/account/edit_userinfo.php',headers=headers).text)
parse()
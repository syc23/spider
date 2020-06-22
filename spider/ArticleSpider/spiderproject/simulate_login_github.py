#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
import time
from selenium import webdriver

def login():
    sess = requests.Session()
    login_url = 'https://github.com/'
    driver = webdriver.Chrome()
    driver.get(login_url)
    time.sleep(3)
    driver.find_element_by_id('user[login]').send_keys('1883245172')
    driver.find_element_by_id('user[email]').send_keys('146734254563@qq.com')
    driver.find_element_by_id('user[password]').send_keys('4234fhsdfs')
    time.sleep(2)
    driver.find_element_by_xpath('//button[@class="btn-mktg btn-primary-mktg btn-large-mktg f4 btn-block my-3"]').click()

    cookies = driver.get_cookies()
    for cookie in cookies:
        print(cookie)
        sess.cookies.set(cookie['name'],cookie['value'])

# login()

def test():
    url = 'https://www.ssyer.com/apis/20001'
    data = {
        "cateId": 1, "page": {"showCount": 20, "currentPage": 1}
    }
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '52',
        'Content-Type': 'application/json',
        'Cookie': 'Cookie: Hm_lvt_8f50334c83664955c1a1a866dd168053=1566567345; _dg_playback.7b6028a56aac520d.ce42=1; _dg_abtestInfo.7b6028a56aac520d.ce42=1; _dg_check.7b6028a56aac520d.ce42=-1; _dg_antiBotFlag.7b6028a56aac520d.ce42=1; _dg_antiBotInfo.7b6028a56aac520d.ce42=10%7C%7C%7C3600; SESSION=NTQ2ODc0YzMtYzc0NS00MWMyLWE2YjEtNWYyNzExNWI0ZGMy; Hm_lpvt_8f50334c83664955c1a1a866dd168053=1566570315; _dg_antiBotMap.7b6028a56aac520d.ce42=201908232225%7C%7C%7C1; _dg_id.7b6028a56aac520d.ce42=2063e474149e6c37%7C%7C%7C1566567346%7C%7C%7C5%7C%7C%7C1566570318%7C%7C%7C1566570315%7C%7C%7C%7C%7C%7C46e637c2cb0b0908%7C%7C%7C%7C%7C%7C%7C%7C%7C1%7C%7C%7Cundefined',
        'Host': 'www.ssyer.com',
        'Origin': 'https://www.ssyer.com',
        'Referer': 'https://www.ssyer.com/cate/1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.post(url, headers=headers, data=data).content.decode()
    print(response)
test()
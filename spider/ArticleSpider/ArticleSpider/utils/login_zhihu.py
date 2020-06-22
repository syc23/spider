#!usr/bin/env python  
#-*- coding:utf-8 -*-
from selenium import webdriver
import time
driver = webdriver.PhantomJS()
driver.get('https://www.baidu.com')
time.sleep(3)
driver.save_screenshot('aa.png')
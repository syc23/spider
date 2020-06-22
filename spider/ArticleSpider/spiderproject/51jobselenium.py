#!usr/bin/env python
#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path=r'C:\Users\acer\Desktop\spider\ArticleSpider\spiderproject\chromdriver\chromedriver.exe')
driver.get("https://www.51job.com/")

driver.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys("python", Keys.ENTER)
div_list = driver.find_element_by_id("resultList").find_elements_by_class_name("el")[1:]
for div in div_list:
    a = div.find_element_by_xpath("p/span/a")
    a.click()
    time.sleep(1)
    # 切换窗口
    driver.switch_to.window(driver.window_handles[-1])
    details = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div')
    print(details.text)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)



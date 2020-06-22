#!usr/bin/env python
#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def getdata():
    driver = webdriver.Chrome(executable_path=r'C:\Users\acer\Desktop\spider\ArticleSpider\spiderproject\chromdriver\chromedriver.exe')
    driver.get("https://www.lagou.com/")
    driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="search_input"]').send_keys("python", Keys.ENTER)
    # 关闭广告弹窗
    driver.find_element_by_xpath('/html/body/div[8]/div/div[2]').click()

    alist = driver.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/h3')
    for a in alist:
        a.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        job_desc = driver.find_element_by_xpath('//*[@id="job_detail"]/dd[2]').text
        print(job_desc)
        print("=====================================")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

if __name__ == '__main__':
    getdata()

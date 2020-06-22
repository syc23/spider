#!usr/bin/env python  
#-*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import cv2 as cv
import numpy as np

def get_position():
    bg = cv.imread('./code_img/bgimg.png')
    front = cv.imread('./code_img/frontimg.png')

    # 灰度处理
    front = cv.cvtColor(front,cv.COLOR_BGR2GRAY)
    front = front[front.any(1)] # 裁剪图像
    bg = cv.cvtColor(bg,cv.COLOR_BGR2GRAY)
    # 滑块匹配
    result = cv.matchTemplate(bg,front,cv.TM_CCOEFF_NORMED)
    _,position = np.unravel_index(result.argmax(),result.shape) # 匹配的位置
    return position

def get_track(distance): # distance为传入的总距离
    # 移动轨迹
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5
    # 计算间隔
    t=0.2
    # 初速度
    v=0
    while current<distance:
        if current<mid:
            # 加速度为2
            a=2
        else:
            # 加速度为-2
            a=-3
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
    return track

def move_to_gap(driver,slider,tracks):  # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.3)
    ActionChains(driver).release().perform()

def click_slide():
    url = "https://dun.163.com/trial/sense"

    driver = webdriver.Chrome(executable_path=r"C:\Users\acer\Desktop\spider\ArticleSpider\spiderproject\chromdriver\chromedriver.exe")
    driver.get(url)
    driver.find_element_by_xpath('//ul[@class="tcapt-tabs__container"]/li[position()=2]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="yidun_intelli-tips"]').click()
    time.sleep(2)

    bg_img = driver.find_element_by_xpath('//img[@class="yidun_bg-img"]').get_attribute('src')
    front_img = driver.find_element_by_xpath('//img[@class="yidun_jigsaw"]').get_attribute('src')

    if bg_img and front_img:
        with open('./code_img/bgimg.png','wb') as f:
            content = requests.get(bg_img).content
            f.write(content)
        with open('./code_img/frontimg.png','wb') as f:
            content = requests.get(front_img).content
            f.write(content)
    else:
        print("acquire img fail !")

    m = get_position()  # 得到滑块移动的位置

    slide = driver.find_element_by_xpath('//div[@class="yidun_slider"]')

    move_to_gap(driver,slide, get_track(m))

    time.sleep(3)

    driver.close()

if __name__ == '__main__':
    click_slide()





#!usr/bin/env python  
#-*- coding:utf-8 -*-
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

cap = {
      "platformName": "Android",
      "platformVersion": "4.4.2",
      "deviceName": "127.0.0.1:62001",
      "appPackage": "com.tal.kaoyan",
      "appActivity": "com.tal.kaoyan.ui.activity.HomeTabActivity",
      "noReset": True
}

driver = webdriver.Remote('http://localhost:4723/wd/hub',cap)

def get_size():
      x = driver.get_window_size()["width"]
      y = driver.get_window_size()["height"]
      return (x,y)

try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_xpath("//android.widget.RadioButton[@resource-id='com.tal.kaoyan:id/mainactivity_button_mysefl']")):
            driver.find_element_by_xpath("//android.widget.RadioButton[@resource-id='com.tal.kaoyan:id/mainactivity_button_mysefl']").click()
            driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/activity_usercenter_username']").click()
except:
      pass

try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_xpath("//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']")):
            driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']").send_keys("syc1314ss")
            driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_password_edittext']").send_keys("147258369syc")
            driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.tal.kaoyan:id/login_login_btn']").click()
except:
      pass

try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_agree']")):
            driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_agree']").click()
            driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.tal.kaoyan:id/date_fix']").click()
except:
      pass

try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_xpath("//android.widget.RadioButton[@resource-id='com.tal.kaoyan:id/mainactivity_button_calendar']")):
            driver.find_element_by_xpath("//android.widget.RadioButton[@resource-id='com.tal.kaoyan:id/mainactivity_button_calendar']").click()
except:
      pass

try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.RelativeLayout[4]/android.widget.LinearLayout[1]/android.widget.ImageView[1]")):
            driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.RelativeLayout[4]/android.widget.LinearLayout[1]/android.widget.ImageView[1]").click()

            size = get_size()
            x1 = int(size[0]*0.5)
            y1 = int(size[1]*0.75)
            y2 = int(size[1]*0.25)
            while True:
                  driver.swipe(x1,y1,x1,y2)
                  time.sleep(1)
except:
      pass


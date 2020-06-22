#!usr/bin/env python  
#-*- coding:utf-8 -*-
from selenium import webdriver
import parsel,time
import json,csv
import pymongo
class Douyu:
    def __init__(self):
        self.start_url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()
    def get_content_list(self):
        source = self.driver.page_source
        sel = parsel.Selector(source)
        content_list = []
        for li in sel.xpath('//section[contains(@class,"layout-Module")]//ul[@class="layout-Cover-list"]/li'):
            item = {}
            item['title'] = li.xpath('.//h3/@title').get()
            item['watch_num'] = li.xpath('.//span[contains(@class,"DyListCover-hot")]//text()').get()
            item['author_name'] = li.xpath('.//h2[contains(@class,"DyListCover-user")]//text()').get()
            item['root_cate'] = li.xpath('.//span[contains(@class,"DyListCover-zone")]/text()').get()
            item['root_img'] = li.xpath('.//img[@class="DyImg-content is-normal"]/@src').get()
            print(item)
            content_list.append(item)
        next_url = self.driver.find_elements_by_xpath('//span[text()="下一页"]')
        next_url = next_url[0] if len(next_url)>0 else None
        return content_list, next_url
    def save_content(self,content_list):
        with open('douyu.json','a',encoding='utf-8') as fp:
            for content in content_list:
                fp.write(json.dumps(content,ensure_ascii=False))
                fp.write('\n')
    def run(self):
        self.driver.get(self.start_url)
        time.sleep(5)
        content_list,next_url = self.get_content_list()
        self.save_content(content_list)
        while next_url is not None:
              next_url.click()
              time.sleep(5)
              content_list,next_url = self.get_content_list()
              self.save_content(content_list)
if __name__ == '__main__':
    douyu = Douyu()
    douyu.run()
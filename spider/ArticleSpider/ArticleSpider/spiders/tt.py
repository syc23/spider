# -*- coding: utf-8 -*-
import scrapy
import time
import json
import copy
class TtSpider(scrapy.Spider):
    def __init__(self):
        self.base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.index = 1
    name = 'tt'
    allowed_domains = ['careers.tencent.com']
    timestamp = int(time.time()*1000)
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(timestamp,1)]
    def parse(self, response):
        item = {}
        content = json.loads(response.text)
        posts = content['Data']['Posts']
        for i in range(len(posts)):
            item['BGName'] = posts[i]['BGName']
            item['CategoryName'] = posts[i]['CategoryName']
            item['CountryName'] = posts[i]['CountryName']
            item['LastUpdateTime'] = posts[i]['LastUpdateTime']
            item['LocationName'] = posts[i]['LocationName']
            item['PostId'] = posts[i]['PostId']
            item['PostURL'] = posts[i]['PostURL']
            item['RecruitPostId'] = posts[i]['RecruitPostId']
            item['RecruitPostName'] = posts[i]['RecruitPostName']
            item['Responsibility'] = posts[i]['Responsibility']
            yield scrapy.Request(url='https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp={}&postId={}&language=zh-cn'.format(int(time.time()*1000),item['PostId']),callback=self.detail,meta={'item':copy.deepcopy(item)})
        self.index+=1
        timestamp = int(time.time()*1000)
        yield scrapy.Request(url=self.base_url.format(timestamp,self.index))
    def detail(self,response):
        item = response.meta['item']
        if response.text:
            content = json.loads(response.text)
            item['Requirement'] = content['Data']['Requirement']
        else:
            item['Requirement'] = None
        print(item)
        print(self.index)
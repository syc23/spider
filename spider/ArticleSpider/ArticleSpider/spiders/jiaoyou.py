# -*- coding: utf-8 -*-
import scrapy
import json

class JiaoyouSpider(scrapy.Spider):
    def __init__(self):
        self.base_url= 'http://www.7799520.com/api/user/pc/list/search?marry=1&page='
    name = 'jiaoyou'
    allowed_domains = ['7799520.com']
    start_urls = ['http://www.7799520.com/api/user/pc/list/search?marry=1&page=1']

    def parse(self, response):
        item = {}
        count =1
        content = json.loads(response.body)['data']['list']
        if not content:
            return
        for i in range(len(content)):
            item['avatar'] = content[i]['avatar']
            item['birthdayyear'] = content[i]['birthdayyear']
            item['city'] = content[i]['city']
            item['education'] = content[i]['education']
            item['gender'] = content[i]['gender']
            item['height'] = content[i]['height']
            item['marry'] = content[i]['marry']
            item['monolog'] = content[i]['monolog']
            item['salary'] = content[i]['salary']
            item['province'] = content[i]['province']
            item['monologflag'] = content[i]['monologflag']
            item['userid'] = content[i]['userid']
            item['detail_url'] = 'http://www.7799520.com/user/{}.html'.format(item['userid'])
            item['username'] = content[i]['username']
        # item(avatar=avatar,birthdayyear=birthdayyear,city=city,education=education,gender=gender, \
        #      height=height,marry=marry,monolog=monolog,salary=salary,province=province, \
        #      monologflag=monologflag,userid=userid,detail_url=detail_url,username=username,)
            print(item)

        count+=1
        yield scrapy.Request(self.base_url+str(count),callback=self.parse,dont_filter=True)

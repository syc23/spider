# -*- coding: utf-8 -*-
import scrapy


class RenrenspiderSpider(scrapy.Spider):
    name = 'renrenspider'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']
    # 发送post请求，需要重写start_request()方法
    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        data = {
            "phone":"18883245153",
            "password":"123"
        }
        request = scrapy.FormRequest(url,formdata=data,callback=self.parse_page)
        yield request
    def parse_page(self,response):
        with open('login.html','w',encoding='utf-8') as f:
            f.write(response.text)

# -*- coding: utf-8 -*-
import scrapy
import scrapy
from jingdong.items import ProductItem
import json
import jsonpath
import copy
import random
import requests
from code_util import ydm
from fake_useragent import FakeUserAgent
import parsel

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://www.jd.com']
    def parse(self, response):
        url = 'https://mall.jd.com/showLicence-10075459.html'
        print(self.get_info(url))
    def get_info(self,url):
        sess = requests.Session()
        code_url = 'https://mall.jd.com/sys/vc/createVerifyCode.html?random={}'.format(random.random())
        img_path = './code.jpg'
        response_ = sess.get(code_url)
        with open(img_path, 'wb') as f:
            f.write(response_.content)
        code = ydm.code(img_path)
        from_data = {
            'verifyCode': code
        }
        headers = {'User-Agent': FakeUserAgent().random}
        response = sess.post(url,data=from_data, headers=headers)
        response.encoding = response.apparent_encoding
        sel = parsel.Selector(response.text)
        name = sel.xpath('//div[@class="jScore"]/ul/li[3]/span/text()').extract_first()
        position = sel.xpath('//div[@class="jScore"]/ul/li[6]/span/text()').extract_first()
        href = sel.xpath('//div[@class="jScore"]/ul/li[12]/span/a/@href').extract_first()
        return name,position,href
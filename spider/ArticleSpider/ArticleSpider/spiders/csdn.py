# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import copy
import jsonpath,json
from scrapy.loader import ItemLoader
from ArticleSpider.items import SinaItem,MyLoader
class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['https://www.csdn.net']
    base_url = 'https://www.csdn.net'

    def parse(self, response):
        cates = response.xpath('//div[@class="nav_com"]/ul/li[not(@class="active")]/a/@href').extract()
        cate_urls = list(map(lambda x:self.base_url+x,cates))
        for url in cate_urls[1:]:
            yield scrapy.Request(url,callback=self.get_shown_offset)
    def get_shown_offset(self,response):
        cate = response.url.split('/')[-1]
        offset = re.findall(r'shown-offset="(.*?)"',response.body.decode())[0]
        detail_url = 'https://www.csdn.net/api/articles?type=more&category={}&shown_offset={}'.format(cate,offset)
        yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'cate':copy.deepcopy(cate)})
    def parse_detail(self,response):
       cate = response.meta['cate']
       url = response.url
       json_content = json.loads(requests.get(url).content.decode())
       next_offset = json_content.get('shown_offset')
       print('*'*40+str(next_offset)+'*'*40)
       detail_link = jsonpath.jsonpath(json_content,'$..url')
       for link in detail_link:
           yield scrapy.Request(link,callback=self.get_content)
       if next_offset:
          yield scrapy.Request(url='https://www.csdn.net/api/articles?type=more&category={}&shown_offset={}'.format(cate,next_offset),callback=self.parse_detail,meta={'cate':copy.deepcopy(cate)})
       else:
           return
    def get_content(self,response):
        load_item = MyLoader(item=SinaItem(),response=response)
        load_item.add_xpath('title','//h1[@class="title-article"]/text()')
        load_item.add_xpath('pub_time','//div[@class="article-bar-top"]//span[@class="time"]/text()')
        load_item.add_xpath('author','//a[@class="follow-nickName"]/text()')
        load_item.add_xpath('watch_num','//span[@class="read-count"]/text()')
        load_item.add_value('url',response.url)
        load_item.add_xpath('content','//div[@id="article_content"]')
        load_item.add_value('_id',response.url.split('/')[-1])
        item = load_item.load_item()
        yield item




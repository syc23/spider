# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re,pprint
from ArticleSpider.items import ZhenaiItem

class ZhenaiSpider(CrawlSpider):
    name = 'zhenai'
    allowed_domains = ['zhenai.com']
    start_urls = ['http://city.zhenai.com/']

    rules = (
        Rule(LinkExtractor(allow=r'http://city\.zhenai\.com/.*'), follow=True),
        Rule(LinkExtractor(allow=r'http://album\.zhenai\.com/u/\d+'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = ZhenaiItem()
        item['url'] = response.url
        item['nickname'] = response.xpath('//h1[@class="nickName"]/text()').get()
        item['_id'] = response.xpath('//div[@class="id"]/text()').get()
        item['_id']= re.findall(r'ID：(\d+)',item['_id'])[0] if re.findall(r'ID：(\d+)',item['_id']) else ''
        item['info'] = ','.join(re.findall(r'div class="des f-cl".*?>(.*?)</div> ',response.body.decode('utf-8'))[0].split('|')).strip() if re.findall(r'div class="des f-cl".*?>(.*?)</div> ',response.body.decode('utf-8')) else ''
        item['img_url'] = response.xpath('//div[@class="top f-cl"]//div[@class="logo f-fl"]/@style').get()
        item['img_url'] = re.findall(r'background-image:url\((.*?)\)',item['img_url'])[0] if item['img_url'] else ''
        item['heart'] = re.sub(r'\n','',response.xpath('//div[@class="m-content-box m-des"]/span/text()').get())
        item['purple_btns'] = re.sub(r'\n','',','.join(response.xpath('//div[@class="purple-btns"]//text()').getall()))
        item['pink_btns'] = re.sub(r'\n','',','.join(response.xpath('//div[@class="pink-btns"]//text()').getall()))
        item['interestion'] = response.xpath('//div[contains(@class,"m-interes")]//div[@class="answer f-fl"]//text()').getall()
        item['interestion'] = ','.join([x for x in item['interestion'] if x != '未填写'])
        item['condition'] = ','.join(response.xpath('//div[contains(@class,"gray-btns")]//text()').getall())

        yield item

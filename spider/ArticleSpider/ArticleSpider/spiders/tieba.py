# -*- coding: utf-8 -*-
import scrapy
import copy
from urllib import parse
from ArticleSpider.items import TiebaItem
import re
class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/f?kw=python&ie=utf-8&pn=0']

    def parse(self, response):
        item = TiebaItem()
        item['img_url'] = []
        a_list = response.xpath('//a[@class="j_th_tit "]')
        for i in a_list:
            item['title'] = i.xpath('./@title').extract_first()
            item['href'] = 'http://tieba.baidu.com'+i.xpath('./@href').extract_first()
            # meta的参数传递是浅拷贝,scrapy是异步框架,会出现值被覆盖，所以使用深拷贝meta={'item':copy.deepcopy(item)
            yield scrapy.Request(url=parse.urljoin('http://tieba.baidu.com',item['href']),callback=self.detail,meta={'item':copy.deepcopy(item)})
        next_url = re.findall(r'<a href="(.*?)" class="next pagination-item " >下一页&gt;</a>',response.body.decode("utf-8"))
        # next_url = response.xpath('//a[@class="next pagination-item "]/@href').extract_first()
        print(next_url)
        if next_url is not None:
            yield scrapy.Request(parse.urljoin('http:',next_url[0]),callback=self.parse)
    def detail(self,response):
        item = response.meta['item']
        pic_url = response.xpath('//img[@class="BDE_Image"]/@src').extract()
        if pic_url is not None:
            item['img_url'].extend(pic_url)
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(url=parse.urljoin('http://tieba.baidu.com',next_url),callback=self.detail,meta={'item':copy.deepcopy(item)})
        yield item
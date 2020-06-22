# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MaoyanSpider(CrawlSpider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/films\?showType=3&offset=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/films/\d+'), callback='parse_detail'),
    )

    def parse_detail(self, response):
        item = {}
        print(response.url)
        # return item

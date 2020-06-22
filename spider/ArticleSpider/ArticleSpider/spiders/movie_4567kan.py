# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import redis
import hashlib
"""
    实现增量式爬虫
"""

class Movie4567kanSpider(CrawlSpider):
    name = 'movie_4567kan'
    allowed_domains = ['4567kan.com']
    start_urls = ['http://www.4567kan.com/index.php/vod/show/id/1/page/1.html']
    redis_cli = redis.Redis()

    rules = (
        Rule(LinkExtractor(allow=r'/vod/show/id/1/page/\d+\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        m = hashlib.md5()
        m.update(response.url.encode())
        if self.redis_cli.sadd('movie_detail_link',m.hexdigest()) ==1:
            print(response.url)
        else:
            print('该网站数据没有更新')

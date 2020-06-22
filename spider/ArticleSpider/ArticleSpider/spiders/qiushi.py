# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import hashlib
import redis
# 增量式爬虫
class QiushiSpider(CrawlSpider):
    name = 'qiushi'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']
    redis_cli = redis.Redis()
    rules = (
        Rule(LinkExtractor(allow=r'/text/page/2/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        for div in response.xpath('//div[@class="col1"]/div'):
            author = div.xpath('./div/a[2]/h2/text()').extract_first().strip()
            content = ''.join(div.xpath('.//div[@class="content"]/span[1]/text()').extract()).strip()
            source = author+content
            source_id = hashlib.sha256(source.encode()).hexdigest()
            if self.redis_cli.sadd('source_id',source_id) == 1:
                print("数据更新了！")
            else:
                print("数据没有更新！")



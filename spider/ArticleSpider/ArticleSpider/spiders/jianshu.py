# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        item['author'] = response.xpath('//span[@class="name"]/a/text()').extract_first()
        item['pub_time'] = response.xpath('//span[@class="publish-time"]/text()').extract_first()
        item['word_num'] = response.xpath('//span[@class="wordage"]/text()').extract_first()
        item['read'] = response.xpath('//span[@class="views-count"]/text()').extract_first()
        item['commment'] = response.xpath('//span[@class="comments-count"]/text()').extract_first()
        item['fav'] = response.xpath('//span[@class="likes-count"]/text()').extract_first()
        item['subjects'] = ','.join(response.xpath('//div[@class="include-collection"]//div[@class="name"]/text()').extract())
        item['comment'] = response.xpath('//div[@class="comment-wrap"]/p/text()').extract()
        with open('test.html','w',encoding='utf-8') as f:
            f.write(response.body.decode())
        return item

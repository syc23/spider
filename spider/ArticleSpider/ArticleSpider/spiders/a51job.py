# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import Job51
import re
from scrapy_redis.spiders import RedisCrawlSpider

class A51jobSpider(RedisCrawlSpider):
    name = '51job'
    allowed_domains = ['51job.com']
    # start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']
    redis_key = 'start_url'

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="el"]//p[@class="t1 "]//a'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="p_in"]//li/a'),follow=True)
    )
    def parse_item(self, response):
        item = Job51()

        item['title'] = response.xpath('//div[@class="cn"]/h1/@title').extract_first()
        item['money'] = response.xpath('//div[@class="cn"]/strong/text()').extract_first()
        item['company'] = response.xpath('//div[@class="cn"]/p/a/@title').extract_first()
        item['msg'] = response.xpath('//p[@class="msg ltype"]/@title').extract_first()
        item['msg'] = re.sub(r'\xa0\xa0','', item['msg'])
        item['address'] = response.xpath('//div[@class="bmsg inbox"]//p[@class="fp"]//text()').extract()[-1] if response.xpath('//div[@class="bmsg inbox"]//p[@class="fp"]//text()').extract() else None
        item['url'] = response.url
        yield item


# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import datetime
from ArticleSpider.items import CfItem
class CfSpider(CrawlSpider):
    name = 'cf'
    allowed_domains = ['bxjg.circ.gov.cn']
    start_urls = ['http://bxjg.circ.gov.cn/web/site0/tab5241/module14458/page1.htm']

    rules = (
        Rule(LinkExtractor(allow=r'/web/site0/tab5241/module14458/page\d+\.htm'),follow=True),
        Rule(LinkExtractor(allow=r'/web/site0/tab5241rr/info\d+\.htm'),callback='parse_item'),
    )

    def parse_item(self, response):
        item = CfItem()
        item['title'] = re.findall(r'<!--TitleStart-->(.*?)<!--TitleEnd-->',response.body.decode('utf-8'))[0].strip()
        item['pub_date'] = datetime.datetime.strptime(re.findall(r'发布时间：(\d{4}-\d{2}-\d{2})',response.body.decode('utf-8'))[0],"%Y-%m-%d")
        item['url'] = response.url
        item['crawl_time'] = datetime.datetime.now()
        yield item

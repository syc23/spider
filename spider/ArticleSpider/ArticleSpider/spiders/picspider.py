# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from ArticleSpider.items import PicItem
class PicspiderSpider(scrapy.Spider):
    name = 'picspider'
    allowed_domains = ['budejie.com']
    start_urls = ['http://www.budejie.com/pic/1']

    def parse(self, response):
        item = PicItem()
        url_list = response.xpath('//img[@class="lazy"]')
        for i in url_list:
            item['pic_url'] = i.xpath('./@data-original').extract()[0]
            yield item

        # 获取下一页链接
        next = response.xpath('//a[@class="pagenxt"]/@href').extract()[0]
        yield scrapy.Request(url=parse.urljoin(response.url,next),callback=self.parse)
        # pass

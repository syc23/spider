# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from urllib import parse
from ArticleSpider.items import ArticleItem,ArticleLoader
from scrapy.loader import ItemLoader
class BlogctoSpider(scrapy.Spider):
    name = 'blogcto'
    allowed_domains = ['blog.51cto.com']
    start_urls = ['https://blog.51cto.com/original/p1']

    def parse(self, response):
        # 提取每篇文章的详情链接
        post_url = response.xpath('//a[@class="tit"]/@href').extract()
        for i in post_url:
            yield scrapy.Request(url=parse.urljoin(response.url,i),callback=self.article_detail)
            break
        # 提取下一页，并交给scrapy进行下载
        next_url = response.xpath('//li[@class="next"]/a/@href').extract()
        if next_url:
            n_url = next_url[0]
            yield scrapy.Request(url=parse.urljoin(response.url,n_url),callback=self.parse)

    def article_detail(self,response):

        # 通过item_loader加载item
        item_loader = ArticleLoader(item=ArticleItem(),response=response)
        item_loader.add_xpath('title','//h1[@class="artical-title"]/text()')
        item_loader.add_xpath('author','//a[@class="name fl"]/text()')
        item_loader.add_xpath('create_date','//a[@class="time fr"]/text()')
        item_loader.add_value('url',response.url)
        item_loader.add_xpath('read_number','//a[@class="read fr"]/text()')
        item_loader.add_xpath('comment_number','//font[@class="comment_number"]/text()')
        item_loader.add_xpath('content','//div[@class="artical-content-bak main-content"]|//div[@class="artical-content-bak main-content editor-side-new"]')
        article_item = item_loader.load_item()

        yield article_item

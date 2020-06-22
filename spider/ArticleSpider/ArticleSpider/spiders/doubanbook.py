# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import parsel
import re

class DoubanbookSpider(CrawlSpider):
    name = 'doubanbook'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']
    rules = (
        Rule(LinkExtractor(allow=r'/tag/\w+',deny='view=cloud')),
        Rule(LinkExtractor(allow=r'/tag/.*\?start=\d+&type=T'),follow=True),
        Rule(LinkExtractor(allow=r'/subject/\d+/'),callback='parse_item'),
    )

    def parse_item(self, response):
        content = response.body.decode('utf-8')
        book_name = re.findall(r'<span property="v:itemreviewed">(.*?)</span>',content,re.S)
        author = re.findall(r'<a href="https://book\.douban\.com/author/\d+/">(.*?)</a>',content,re.S)
        press = re.findall(r'<span class="pl">出版社:</span>(.*?)<br/>',content,re.S)
        pub_date = re.findall(r'<span class="pl">出版年:</span>(.*?)<br/>', content, re.S)
        page_num = re.findall(r'<span class="pl">页数:</span>(.*?)<br/>', content, re.S)
        price = re.findall(r'<span class="pl">定价:</span> (.*?)<br/>', content, re.S)
        bind = re.findall(r' <span class="pl">装帧:</span> (.*?)<br/>', content, re.S)
        blong_to = re.findall(r'<span class="pl">丛书:</span>\s;<a href=".*?">(.*?)</a><br>', content, re.S)
        isbn = re.findall(r' <span class="pl">ISBN:</span>(.*?)<br/>',content,re.S)
        print(author)
        print('')
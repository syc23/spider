# -*- coding: utf-8 -*-
import scrapy
import copy
import json
from urllib import parse
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']
    # 获取不同种类的图书详情链接
    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt') #大分类list
        for dt in dt_list:
            item = {}
            item['b_cate'] = 'https:'+dt.xpath('./a/@href').extract_first()
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            for em in em_list:
                item['s_href'] = em.xpath('./a/@href').extract_first()
                item['s_cate'] = em.xpath('./a/text()').extract_first()
                if item['s_href'] is not None:
                    item['s_href'] = 'https:'+item['s_href']
                    yield scrapy.Request(url=item['s_href'],callback=self.parse_book_list,meta={'item':copy.deepcopy(item)})
    # 获取商品详情
    def parse_book_list(self,response):
        item = response.meta['item']
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        for li in li_list:
            item['book_url'] = 'https:'+li.xpath('.//div[@class="p-img"]/a/@href').extract_first()
            item['book_img'] = li.xpath('.//div[@class="p-img"]//img/@src').extract_first()
            if item['book_img'] is not None:
                item['book_img'] = 'https:'+li.xpath('.//div[@class="p-img"]/a/img/@src').extract_first()
            else:
                item['book_img'] = 'https:'+li.xpath('.//div[@class="p-img"]//img/@data-lazy-img').extract_first()
            item['book_name'] = li.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            item['book_author'] = li.xpath('.//span[@class="p-bi-name"]/span/a/@title').extract()
            item['book_press'] = li.xpath('.//span[@class="p-bi-store"]/a/@title').extract_first()
            item['book_pub_date'] = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()
            item['book_sku'] = li.xpath('./div/@data-sku').extract_first()
            # 获取商品价格
            yield scrapy.Request(url='https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['book_sku']),callback=self.parse_book_price,meta={'item':copy.deepcopy(item)})

        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(url=parse.urljoin(response.url,next_url),callback=self.parse_book_list,meta={'item':copy.deepcopy(item)})
    # 获取商品价格
    def parse_book_price(self,response):
        item = response.meta['item']
        item['book_price'] = json.loads(response.text)[0]['op']
        print(item)


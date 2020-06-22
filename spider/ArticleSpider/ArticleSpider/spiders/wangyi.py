# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    start_urls = ['https://war.163.com/']

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome()

    def parse(self, response):
        for div in response.xpath('//div[@class="ndi_main"]/div'):
            title  = div.xpath('./div[@class="news_title"]/h3/a/text()').extract_first()
            article_link = div.xpath('./div[@class="news_title"]/h3/a/@href').extract_first()
            print(title)
    def close(self, spider):
        self.driver.close()
        print("爬虫结束了！")


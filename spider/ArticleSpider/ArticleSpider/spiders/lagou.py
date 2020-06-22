# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime,re
from ArticleSpider.items import LagouItem
class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/','https://www.lagou.com/gongsi/','https://xiaoyuan.lagou.com/']
    rules = (
        Rule(LinkExtractor(allow=r'/jobs/list_.*\?isSchoolJob=1'), follow=True),
        Rule(LinkExtractor(allow=r'/zhaopin/.*/'), follow=True),
        Rule(LinkExtractor(allow=r'/gongsi/j\d+\.html'),follow=True),
        Rule(LinkExtractor(allow=r'/jobs/\d+\.html',deny=(r'utrack/trackMid\.html')), callback='parse_item', follow=True),
    )

    def deal_str(self,value):
        if value:
            return re.sub(r'\/|\s|\xa0|发布于拉勾网|查看地图|,|,', '', value).strip()
        else:
            return ''
    def parse_item(self, response):
           item = LagouItem()
           title = response.xpath('//h2[@class="name"]/text()').extract()
           url = response.url
           url_object_id = url.split('/')[-1].split('.')[0]
           salary = response.xpath('//span[@class="salary"]/text()').extract()
           job_city = response.xpath('//dd[@class="job_request"]/h3/span[2]/text()').extract()
           work_years = response.xpath('//dd[@class="job_request"]/h3/span[3]/text()').extract()
           degree_need = response.xpath('//dd[@class="job_request"]/h3/span[4]/text()').extract()
           job_type = response.xpath('//dd[@class="job_request"]/h3/span[5]/text()').extract()
           publish_time = response.xpath('//p[@class="publish_time"]/text()').extract()
           job_advantage = response.xpath('//dd[@class="job-advantage"]/p/text()').extract()
           job_desc = response.xpath('//div[@class="job-detail"]/p//text()').extract()
           job_addr = response.xpath('//div[@class="work_addr"]//text()').extract()
           company_name = response.xpath('//a[@data-lg-tj-track-code_util="jobs_logo"]/img/@alt').extract()
           company_url = response.xpath('//a[@data-lg-tj-track-code_util="jobs_logo"]/@href').extract()
           tags = response.xpath('//ul[contains(@class,"position-label")]/li//text()').extract()
           crawl_time = datetime.datetime.now()
           yield item
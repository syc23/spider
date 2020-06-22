# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
from ArticleSpider.items import Yangguang
class YangguangSpider(scrapy.Spider):
    name = 'yangguang'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/report?page=59621']

    def parse(self, response):

        for url in  response.xpath('//a[@class="news14"]/@href').extract():
            yield scrapy.Request(url,callback=self.detail)
        # 翻页
        next_url = response.xpath('//a[text()=">"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.parse)


    def detail(self,response):
        item  = Yangguang()
        # item_loader = ItemLoader(item=Yangguang(), response=response)
        # 获取名称
        title = response.xpath('//div[@class="wzy1"]//span[@class="niae2_top"]').extract_first()
        if title:
            item['title'] = re.sub('</span>',"",title.split('：')[-1].strip().replace(' ',''))
        else:
            tit = response.xpath('//div[@class="pagecenter p3"]//div[@class="greyframe"]//div[@class="cleft"]//strong[@class="tgray14"]/text()').extract_first()
            rg = r'.*?：(.*?)  .*?:.*'
            item['title'] = re.match(rg,tit).group(1)
        # 获取编号
        id = response.xpath('//div[@class="wzy1"]//span[2]').extract_first()
        if id is not None:
            item['number_id'] = int(re.sub('</span>',"",id.split(':')[-1].strip()))
        else:
            regs = r'.*?：.*?  .*?:(.*)'
            ids = response.xpath('//div[@class="pagecenter p3"]//div[@class="greyframe"]//div[@class="cleft"]//strong[@class="tgray14"]/text()').extract_first()
            item['number_id'] = int(re.match(regs,ids).group(1).replace('\xa0\xa0',""))
        # 作者和发布时间
        base = response.xpath('//div[@class="wzy3_2"]//span[1]').extract_first()
        if base is not None:
            reg = r'.*?：(.*?) .*：(\d+-\d+-\d+ \d+:\d+:\d+).*'
            item['author'] = re.match(reg,base).group(1)
            item['pub_date'] = datetime.datetime.strptime(re.match(reg,base).group(2),"%Y-%m-%d %H:%M:%S")
            # item['pub_date'] = re.match(reg, base).group(2)
        else:
            authors = response.xpath('//div[@class="content text14_2"]//div[@class="audit"]//div[@class="cright"]/p[@class="te12h"]/text()').extract_first()
            reggs = r'.*：(.*?) .*：(.*?)  '
            item['author'] = re.match(reggs,authors).group(1)
            item['pub_date'] = datetime.datetime.strptime(re.match(reggs, authors).group(2),"%Y-%m-%d %H:%M:%S")
        # 内容及其内容相关图片
        pic_url = response.xpath('//div[@class="textpic"]/img/@src').extract()
        if pic_url:
            item['content'] = re.sub('\xa0|\s',"",response.xpath('//div[@class="contentext"]/text()').extract_first().strip().replace('</span>'," "))
            item['img_url'] = ['http://wz.sun0769.com'+url for url in pic_url]
        else:
            item['content'] = re.sub('\xa0|\s',"",response.xpath('//td[@class="txt16_3"]/text()|//div[@class="c1 text14_2"]/text()').extract_first().strip().replace('</span>'," "))
            item['img_url'] = None

        item['url'] = response.url
        yield item


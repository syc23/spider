# -*- coding: utf-8 -*-
import scrapy
import jsonpath
import json
import string,random
import re
from copy import deepcopy
class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com','openapi-vtom.vmovier.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']
    cookies = dict(Authorization='C3A13D6ADB440C569DB4404F38DB440B111DB440323ED2580136')
    f = open('./discover.json', 'a', encoding='utf-8')
    count = 0
    def gen_sessid(self):
        return random.choices(string.ascii_lowercase+string.digits,k=26)
    def parse(self, response):
        print(response.url)
        self.count+=1
        if self.count%20==0:
            self.cookies.update(PHPSESSID=self.gen_sessid())
        item = {}
        articleid = response.xpath('//ul[@class="video-list"]/li/@data-articleid').extract()
        for a_id in articleid:
            url = 'https://www.xinpianchang.com/a{}?from=ArticleList'.format(a_id)
            item['a_id'] = a_id
            yield scrapy.Request(url,callback=self.parse_post,meta={'item':deepcopy(item)})
        next_url = response.xpath('//a[@title="下一页"]/@href').get()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url),callback=self.parse,cookies=self.cookies)
    def parse_post(self,response):
        item = response.meta['item']
        category1 = response.xpath('//span[contains(@class,"cate")][1]//text()').getall()
        category2 = response.xpath('//span[contains(@class,"cate")][2]//text()').getall()
        category2 = self.deal_category(category2) if category2 else ''
        item['category'] = re.sub(r'\n|\t','',''.join(category1)) + category2
        item['update_time'] = response.xpath('//span[contains(@class,"update-time")]/i/text()').get()
        item['play_number'] = response.xpath('//i[contains(@class,"play-counts")]/@data-curplaycounts').get()
        item['like_counts'] = response.xpath('//span[contains(@class,"like-counts")]/@data-counts').get()
        item['desc_info'] = response.xpath('//p[contains(@class,"desc line-hide")]/text()').get().strip() if response.xpath('//p[contains(@class,"desc line-hide")]/text()').get() else ''
        item['tags'] = ','.join([i.strip() for i in response.xpath('//div[contains(@class,"tag-wrapper")]//text()').getall()]) if response.xpath('//div[contains(@class,"tag-wrapper")]//text()').getall() else ''
        vid, = response.selector.re(r'vid: "(.*?)"')
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/{}?expand=resource&usage=xpc_web'.format(vid)
        yield scrapy.Request(video_url,callback=self.parse_video,meta={'item':deepcopy(item)})
    def parse_video(self,response):
        item = response.meta['item']
        content = json.loads(response.text)
        item['video_name'] = jsonpath.jsonpath(content,'$..title')[0] if jsonpath.jsonpath(content,'$..title') else ''
        item['video_url'] = jsonpath.jsonpath(content,'$..resource.default.url')[0] if jsonpath.jsonpath(content,'$..resource.default.url') else ''
        item['preview'] = jsonpath.jsonpath(content,'$..cover')[0] if jsonpath.jsonpath(content,'$..title') else ''
        item['duration'] = jsonpath.jsonpath(content, '$..duration')[0] if jsonpath.jsonpath(content, '$..duration') else ''
        comments_url = 'https://app.xinpianchang.com/comments?resource_id={}&type=article&page=1'.format(item['a_id'])
        yield scrapy.Request(response.urljoin(comments_url),callback=self.parse_comment,meta={'item':deepcopy(item)})
    def parse_comment(self,response):
        item = response.meta['item']
        comments = {}
        comments['a_id'] = response.meta['item'].get('a_id')
        content = json.loads(response.text)
        comments['content'] = self.deal_none(jsonpath.jsonpath(content,'$..list..content'))
        comments['addtime'] = self.deal_none(jsonpath.jsonpath(content, '$..list..addtime'))
        comments['count_approve'] = self.deal_none(jsonpath.jsonpath(content, '$..list..count_approve'))
        comments['avatar'] = self.deal_none(jsonpath.jsonpath(content, '$..list..avatar'))
        comments['occupation'] = self.deal_none(jsonpath.jsonpath(content, '$..list..occupation'))
        comments['sex'] = self.deal_none(jsonpath.jsonpath(content, '$..list..sex'))
        comments['username'] = self.deal_none(jsonpath.jsonpath(content, '$..list..username'))
        comments['userid'] = self.deal_none(jsonpath.jsonpath(content, '$..list..userid'))
        comments['verify_description'] = self.deal_none(jsonpath.jsonpath(content, '$..list..verify_description'))
        comments['web_url'] = self.deal_none(jsonpath.jsonpath(content, '$..list..web_url'))
        item['comments'] = comments
        print(item)
        line = json.dumps(item,ensure_ascii=False)
        self.f.write(line+'\n')

        next_urls = jsonpath.jsonpath(content,'$..next_page_url')
        if next_urls:
           for next_url in next_urls:
               yield scrapy.Request(response.urljoin(next_url),callback=self.parse_comment,meta={'item':deepcopy(item)})

    def deal_none(self,value):
        return value[0] if value else ''
    def deal_category(self,category):
        category = ' | ' + re.sub(r'\n|\t', '', ''.join(category)) if category else ''
        return category
    def close(spider, reason):
        spider.f.close()
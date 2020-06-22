# -*- coding: utf-8 -*-
import scrapy
import re
import copy
from urllib import parse
class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com','esf.fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']
    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_text = tds[0].xpath('.//text()').extract_first()
            province_text = re.sub('\s','',province_text)
            if province_text:
                province = province_text
            if province =="其它":
                continue
            for a in tds[1].xpath('.//a'):
                city = a.xpath('.//text()').extract_first()
                city_link = a.xpath('.//@href').extract_first()
                url_model = re.split('//',city_link)
                scheme = url_model[0]
                domain = url_model[1]
                city_id = domain.split('.')[0]
                if 'bj.' in domain:
                    new_house_link = 'https://newhouse.fang.com/house/s/'
                    esf_link = 'https://esf.fang.com/'
                else :
                    # 构建新房链接
                    new_house_link = scheme+'//'+city_id+'.newhouse.'+'fang.com/house/s/'
                    # 构建二手房链接
                    # esf_link = scheme+'//'+'city_id'+domain
                    esf_link = 'https://{}.zu.fang.com/house/a21/'.format(city_id)
                    print(esf_link)
                # yield scrapy.Request(url=new_house_link,callback=self.parse_newhouse,\
                #             meta={'info':copy.deepcopy((province,city))})
                # yield scrapy.Request(url=esf_link,callback=self.parse_esf,dont_filter=True,meta={'info': copy.deepcopy((province, city))})
                break
            break
    def parse_newhouse(self,response):
        # item = {}
        # province,city = response.meta['info']
        # item['provice'] = province
        # item['city'] = city
        # li_list = response.xpath('//div[contains(@class,"nl_con")]/ul/li')
        # for li in li_list:
        #     item['name'] = li.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first()
        #     if item['name']:
        #         item['name'] = item['name'].strip()
        #     item['price'] = li.xpath('.//div[contains(@class,"nhouse_price")]//text()').extract()
        #     if item['price']:
        #         item['price'] = re.sub('\s|\n|\t|广告','',''.join(item['price']))
        #     else:
        #         item['price'] = ''
        #     if li.xpath('.//div[contains(@class,"house_type")]/a/text()').extract():
        #         item['rooms'] = ','.join(list(filter(lambda x:x.endswith("居"),li.xpath('.//div[contains(@class,"house_type")]/a/text()').extract())))
        #     area = li.xpath('.//div[contains(@class,"house_type")]/text()').extract()
        #     if area:
        #         item['area'] = re.sub('\n|\t|\s|/|－', '', ''.join(area))
        #     else:
        #         item['area'] =''
        #     item['address'] = li.xpath('.//div[contains(@class,"address")]/a/@title').extract_first()
        #     district = re.sub('\n|\t|\s','',''.join(li.xpath('.//div[contains(@class,"address")]/a//text()').extract()))
        #     item['district'] = re.findall(r'.*\[(.+)\].*',district,re.S)
        #     if item['district']:
        #         item['district'] = item['district'][0]
        #     item['detail_link'] = li.xpath('.//div[contains(@class,"address")]/a/@href')
        #     if item['detail_link']:
        #         item['detail_link'] = 'https:'+item['detail_link'].extract_first()
        #     else:
        #         item['detail_link'] = ''
        #     item['sale'] = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').extract_first()
        #     yield item
        #     print(item)

        print(response.url)
        # next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        # # if next_url:
        # #     yield scrapy.Request(url=parse.urljoin(response.url,next_url),callback=self.parse_newhouse,meta={'info':copy.deepcopy((province,city))})
    def parse_esf(self,response):
        print(response.url)
        # item = {}
        # province, city = response.meta['info']
        # item['provice'] = province
        # item['city'] = city
        # dls = response.xpath('//div[contains(@class,"shop_list")]/dl')
        # for dl in dls:
        #     name = dl.xpath('./dd//a/span/text()').extract_first()
        #     if name:
        #        item['name'] = name.strip()
        #     else:
        #         item['name'] = ''
        #     info = ','.join(dl.xpath('.//p[@class="tel_shop"]/text()').extract())
        #
        #     if info:
        #         infos = re.sub('\r|\n|\s','',info).split(',')
        #         rooms = None
        #         area = None
        #         toward = None
        #         floor = None
        #         year = None
        #         for inf in infos:
        #             if '厅' in inf:
        #                 rooms = inf
        #             elif 'm' in inf:
        #                 area = inf
        #             elif '层' in inf:
        #                  floor = inf
        #             elif '向' in inf:
        #                 toward = inf
        #             else :
        #                 year = inf
        #         print(rooms, area, floor, toward, year)

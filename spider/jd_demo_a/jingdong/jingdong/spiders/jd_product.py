# -*- coding: utf-8 -*-
import scrapy
from jingdong.items import ProductItem
import json
import jsonpath
import copy
import random
import requests
from code_util import ydm
from fake_useragent import FakeUserAgent
import parsel
class JdProductSpider(scrapy.Spider):
    name = 'jd_product'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = [i.strip('\n') for i in open('./url.txt','r').readlines()]
    def parse(self, response):
        try:
            sku_ids = response.xpath('//div[contains(@class,"j-sku-item")]/@data-sku').extract()
            item = ProductItem()
            for sku in sku_ids:
                item['product_sku_id'] = sku
                product_base_url = 'https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.0/{}.json'.format(sku)
                yield scrapy.Request(product_base_url,callback=self.parse_product_base,meta={'item':copy.deepcopy(item)})
            next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
            if next_url:
               next_url = response.urljoin(next_url)
               yield scrapy.Request(next_url,callback=self.parse)
        except Exception as e:
            pass
    # 解析商品基本信息
    def parse_product_base(self,response):
        item = response.meta['item']
        try:
            result = json.loads(response.text)
            shop = jsonpath.jsonpath(result,'$..shop')
            item['product_name'] = result['wareInfo']['basicInfo']['name']
            if shop:
                shop = shop[0]
                if shop:
                    item['product_shop'] = shop['name']
                    item['shop_url'] = shop['url'].replace('ok','mall')+'l'
                else:
                    item['product_shop'] = '京东自营'
                    item['shop_url'] = ''
            item['product_category_id'] = result['wareInfo']['basicInfo']['category'].replace(';',',')
        except Exception as e:
            pass
        # 促销信息url
        ad_url = 'https://cd.jd.com/promotion/v2?skuId={}&area=24_2222_2228_0&shopId=1000001095&cat={}'.format(item['product_sku_id'],item['product_category_id'])
        yield scrapy.Request(ad_url,callback=self.parse_product_ad,meta={'item':copy.deepcopy(item)})
    # 解析商品促销信息
    def parse_product_ad(self,response):
        try:
            item = response.meta['item']
            result = json.loads(response.body.decode('gbk'))
            # item['product_ad'] = jsonpath.jsonpath(result,'$..ad')[0] if jsonpath.jsonpath(result,'$..ad') else ''
            item['ad_name'] = ','.join(jsonpath.jsonpath(result, '$..name')) if jsonpath.jsonpath(result, '$..name') else ''
            # 请求价格url
            price_url = 'https://p.3.cn/prices/mgets?&skuIds=J_{}'.format(item['product_sku_id'])
            yield scrapy.Request(price_url, callback=self.parse_product_price, meta={'item': copy.deepcopy(item)})
        except Exception as e:
            pass
    # 解析商品价格信息
    def parse_product_price(self,response):
        try:
            item = response.meta['item']
            result = json.loads(response.text)
            item['product_price'] = result[0]['p']
            yield item
            print(item)
            print('*' * 40)
            # shop_url = item['shop_url']
            # if shop_url:
            #     yield scrapy.Request(shop_url,callback=self.parse_shop_card_id,meta={'item': copy.deepcopy(item)})
        except Exception as e:
            pass
    def parse_shop_card_id(self,response):
        item = response.meta['item']
        try:
            if '京东' not in item['product_shop']:
                shopId = response.selector.re('shopId = "(.*?)"')[0] if response.selector.re('shopId = "(.*?)"') else None
                shop_crad_url = 'https://mall.jd.com/showLicence-{}.html'.format(shopId)
                name,position,href = self.get_info(shop_crad_url)
                item['name'] = name if name else ''
                item['position'] = position if position else ''
                item['href'] = 'https:' + href if href else ''
            else:
                item['name'] = ''
                item['position'] = ''
                item['href'] = ''
            yield item
            print(item)
            print('*' * 40)
        except Exception as e:
            pass
    def get_info(self,url):
        try:
            sess = requests.Session()
            code_url = 'https://mall.jd.com/sys/vc/createVerifyCode.html?random={}'.format(random.random())
            img_path = './code.jpg'
            response_ = sess.get(code_url)
            with open(img_path, 'wb') as f:
                f.write(response_.content)
            code = ydm.code(img_path)
            from_data = {
                'verifyCode': code
            }
            headers = {'User-Agent': FakeUserAgent().random}
            response = sess.post(url,data=from_data, headers=headers)
            response.encoding = response.apparent_encoding
            sel = parsel.Selector(response.text)
            name = sel.xpath('//div[@class="jScore"]/ul/li[3]/span/text()').extract_first()
            position = sel.xpath('//div[@class="jScore"]/ul/li[6]/span/text()').extract_first()
            href = sel.xpath('//div[@class="jScore"]/ul/li[12]/span/a/@href').extract_first()
            return name,position,href
        except Exception as e:
            pass

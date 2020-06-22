# -*- coding: utf-8 -*-
import scrapy
from jingdong.items import ProductItem
import json
import jsonpath
import copy
import pickle
from scrapy_redis.spiders import RedisSpider

class JdProductDistributedSpider(RedisSpider):
    name = 'jd_product_distributed'
    allowed_domains = ['jd.com','p.3.cn']
    redis_key = 'jd_product_distributed:start_url'

    def make_request_from_data(self, data):
        """
        根据redis中读取的分类信息的二进制数据，构建请求
        :param data: 分类信息的二进制数据
        :return: 根据小分类的url，构建请求对象
        """
        category = pickle.loads(data)
        # 这里需要用return一个请求，不能使用yield
        try:
            return scrapy.Request(url=category['s_category_url'],callback=self.parse,meta={'category':copy.deepcopy(category)})
        except:
            pass
    def parse(self, response):
        category = response.meta['category']
        sku_ids = response.xpath('//div[contains(@class,"j-sku-item")]/@data-sku').extract()
        item = ProductItem()
        try:
            for sku in sku_ids:
                item['product_category'] = category
                item['product_sku_id'] = sku
                product_base_url = 'https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.0/{}.json'.format(sku)
                yield scrapy.Request(product_base_url,callback=self.parse_product_base,meta={'item':copy.deepcopy(item),'dont_redirect': True,'handle_httpstatus_list': [302]})
            next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
            if next_url:
               next_url = response.urljoin(next_url)
               yield scrapy.Request(next_url, callback=self.parse, meta={'category': copy.deepcopy(category)})
        except:
            pass
    # 解析商品基本信息
    def parse_product_base(self,response):
        item = response.meta['item']
        try:
            result = json.loads(response.text)
            item['product_name'] = result['wareInfo']['basicInfo']['name']
            item['product_img_url'] = result['wareInfo']['basicInfo']['wareImage'][0]['small']
            item['product_book_info'] = result['wareInfo']['basicInfo']['bookInfo']
            colorSize = jsonpath.jsonpath(result,'$..colorSize')
            if colorSize:
               colorSize = colorSize[0]
               product_option = {}
               for option in colorSize:
                   title = option['title']
                   value = jsonpath.jsonpath(option,'$..text')
                   product_option[title] = value
               item['product_option'] = product_option
            shop = jsonpath.jsonpath(result,'$..shop')
            if shop:
                shop = shop[0]
                if shop:
                    item['product_shop'] ={
                        'shop_id': shop['shopId'],
                        'shop_name': shop['name'],
                        'shop_score': shop['score'],
                        "shop_url": shop['url'],
                        "shop_logo": shop['logo'],
                        "shop_followCount": shop['followCount'],
                        "shop_newNum": shop['newNum'],
                        "shop_promotionNum":shop['promotionNum'],
                    }
                else:
                    item['product_shop'] = {
                        'shop_name': '京东自营'
                    }
            item['product_category_id'] = result['wareInfo']['basicInfo']['category'].replace(';',',')
        except:
            pass
        # 促销信息url
        ad_url = 'https://cd.jd.com/promotion/v2?skuId={}&area=24_2222_2228_0&shopId=1000001095&cat={}'.format(item['product_sku_id'],item['product_category_id'])
        yield scrapy.Request(ad_url,callback=self.parse_product_ad,meta={'item':copy.deepcopy(item)})
    # 解析商品促销信息
    def parse_product_ad(self,response):
        item = response.meta['item']
        try:
            result = json.loads(response.body.decode('gbk'))
            item['product_ad'] = jsonpath.jsonpath(result,'$..ad')[0] if jsonpath.jsonpath(result,'$..ad') else ''
            # 构建请求评论信息的url
            comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.format(item['product_sku_id'])
            yield scrapy.Request(comment_url,callback=self.parse_comment_info,meta={'item':copy.deepcopy(item)})
        except:
            pass
    # 解析商品评论信息
    def parse_comment_info(self,response):
        item = response.meta['item']
        try:
            result = json.loads(response.text)

            comment_info = {
                # 评论数量
                'CommentCount' : jsonpath.jsonpath(result,'$..CommentCount')[0],
                # 好评数量
                'GoodCount': jsonpath.jsonpath(result,'$..GoodCount')[0],
                # 好评率
                'GoodRate': jsonpath.jsonpath(result,'$..GoodRate')[0],
                # 差评数量
                'PoorCount': jsonpath.jsonpath(result,'$..PoorCount')[0],
            }
            item['product_comments'] = comment_info
            # 请求价格url
            price_url = 'https://p.3.cn/prices/mgets?&skuIds=J_{}'.format(item['product_sku_id'])
            yield scrapy.Request(price_url,callback=self.parse_product_price,meta={'item':copy.deepcopy(item)})
        except:
            pass
    # 解析商品价格信息
    def parse_product_price(self,response):
        item = response.meta['item']
        try:
            result = json.loads(response.text)

            item['product_price'] = result[0]['p']
        except:
            pass
        yield item

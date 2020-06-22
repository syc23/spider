# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jingdong.spiders.jd import JdSpider
from jingdong.spiders.jd_product import JdProductSpider
import csv
import MySQLdb
from jingdong import settings
from jingdong.spiders.jd_product_distributed import JdProductDistributedSpider
import pymongo
class CategoryPipeline(object):
    def open_spider(self,spider):
       if isinstance(spider,JdSpider):
           self.f = open('./url.txt','a',encoding='utf-8')
    def process_item(self, item, spider):
        if isinstance(spider, JdSpider):
            print(item['s_category_url'])
            self.f.write(item['s_category_url']+'\n')
        return item
    def close_spider(self,spider):
        if isinstance(spider, JdSpider):
            self.f.close()

class ProductPipeline(object):
    def open_spider(self,spider):
       if isinstance(spider,JdProductSpider):
           self.f = open('./product.csv',mode='a',encoding='utf-8',newline='')
           self.writer = csv.writer(self.f)
    def process_item(self, item, spider):
        if isinstance(spider, JdProductSpider):
            product_price = item['product_price']
            product_name = item['product_name']
            product_shop = item['product_shop']
            ad = item['ad_name']
            cpmpany_name = item['name']
            position = item['position']
            shop_url = item['href']
            self.writer.writerow([product_price,product_name,product_shop,ad,cpmpany_name,position,shop_url])
            self.f.flush()
        return item
    def close_spider(self,spider):
        if isinstance(spider, JdSpider):
            self.f.close()

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host=settings.LOCALHOST,port=settings.PORT,user=settings.USER,passwd = settings.PASSWD,db=settings.DB,charset=settings.CHARSET)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        if isinstance(spider, JdProductSpider):
            product_price = item['product_price']
            product_name = item['product_name']
            product_shop = item['product_shop']
            ad = item['ad_name']
            # company_name = item['name']
            # positions = item['position']
            shop_url = item['shop_url']
            sql = 'insert into products(product_price,product_name,product_shop,ad,shop_url) values(%s,%s,%s,%s,%s)'
            values = (product_price,product_name,product_shop,ad,shop_url)
            self.cursor.execute(sql, values)
            self.conn.commit()
            return item
    def close_spider(self, spider):
        if isinstance(spider, JdProductSpider):
            self.cursor.close()
            self.conn.close()
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jingdong.spiders.jd import JdSpider
from jingdong.spiders.jd_product_distributed import JdProductDistributedSpider
import pymongo
class CategoryPipeline(object):
    def open_spider(self,spider):
       if isinstance(spider,JdSpider):
           self.client = pymongo.MongoClient()
           self.db = self.client.jd.category
    def process_item(self, item, spider):
        if isinstance(spider, JdSpider):
            self.db.insert_one(dict(item))
        return item
    def close_spider(self,spider):
        if isinstance(spider, JdSpider):
            self.client.close()

class ProductPipeline(object):
    def open_spider(self,spider):
       if isinstance(spider,JdProductDistributedSpider):
           self.client = pymongo.MongoClient()
           self.db = self.client.jd.product
    def process_item(self, item, spider):
        if isinstance(spider, JdProductDistributedSpider):
            self.db.insert_one(dict(item))
        return item
    def close_spider(self,spider):
        if isinstance(spider, JdProductDistributedSpider):
            self.client.close()
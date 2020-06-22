# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import scrapy
import os
import MySQLdb
import pymongo
from ArticleSpider import settings
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
# 常规写法
class DemoPipeline(object):
    def __init__(self,path):
        self.f = None
        self.path = path
    @classmethod
    def from_crawler(cls,crawler):
        path = crawler.settings.get('PATH')
        return cls(path)
    def open_spider(self,spider):
        self.f = open(self.path,'w')
    def process_item(self, item, spider):
        return item
    def spider_closed(self, spider):
        pass
# 使用JsonLinesItemExporter类保存数据
from scrapy.exporters import JsonLinesItemExporter
class ArticleExportPipeline(object):
    def __init__(self):
        self.fp = open('tieba.json','wb')
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False)
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item
    def spider_closed(self,spider):
        self.fp.close()

class ArticleJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('sina.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()
class ArticleTxtPipeline(object):
    def __init__(self):
        self.file = open('zhenai.txt','a',encoding='utf-8')
    def process_item(self,item,spider):
        nickname = item['nickname']
        url = item['url']
        _id = item['_id']
        info = item['info']
        img_url = item['img_url']
        heart = item['heart']
        purple_btns = item['purple_btns']
        pink_btns = item['pink_btns']
        interestion = item['interestion']
        condition = item['condition']
        lines = nickname + url + _id + info + img_url + heart + purple_btns + pink_btns + interestion + condition+'\n'
        print(lines)
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()
class ArticleMongodbPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['spider']['lagou']
    def process_item(self,item,spider):
        print(item['title'])
        self.db.insert(dict(item))
        return item
class ArticleMysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host=settings.LOCALHOST,port=settings.PORT,user=settings.USER,passwd = settings.PASSWD,db=settings.DB,charset=settings.CHARSET)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):

        keys,values = zip(*dict(item).items())
        sql = 'insert into cf({}) values({})'.format(','.join(keys),','.join(['%s']*len(values)))
        self.cursor.execute(sql, values)
        self.conn.commit()
        # 打印输出日志
        # spider.logger.info(item)
        return item  # 不return的情况下，另一个权重较低的pipeline就不会获取到该iten

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

class BudejieImagePipeline(ImagesPipeline):
        pass
    # # 重写这个方法主要是为了获取item，使得file_path（）函数能获取到item
    # def get_media_requests(self, item, info):
    #     # 这个方法是在发送下载请求之前调用
    #     # 这个方法本身就是发送下载请求
    #     request_objs = super(BudejieImagePipeline,self).get_media_requests(item,info)
    #     for request_obj in request_objs:
    #         request_obj.item = item
    #  #改写scrapy默认的存储路径
    # def file_path(self, request, response=None, info=None):
    #     # 这个方法是在图片将要被存储的时候调用，来获取这个图片的存储路径
    #     path = super(BudejieImagePipeline,self).file_path(request,response,info)
    #     category = request.item.get('category')
    #     images_store = settings.IMAGES_STORE
    #     category_path = os.path.join(images_store,category)
    #     if not os.path.exists(category_path):
    #         os.makedirs(category_path)
    #     image_name = path.replace("full/","")
    #     image_path = os.path.join(category_path,image_name)
    #     return image_path

    # def get_media_requests(self, item, info):
    #     picurl = item['pic_url']
    #     yield scrapy.Request(picurl)


    # def get_media_requests(self, item, info):
    #     for image_url in item['image_urls']:
    #         yield scrapy.Request(image_url,meta={'image_name':item['image_name']})
    #
    # def file_path(self, request, response=None, info=None):
    #     file_name = request.meta['image_name']+'.jpg'
    #     return file_name
    #



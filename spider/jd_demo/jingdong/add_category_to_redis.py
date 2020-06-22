#!usr/bin/env python  
#-*- coding:utf-8 -*-
import pymongo
import redis
import pickle
from jingdong.spiders.jd_product_distributed import JdProductDistributedSpider
"""
    1、连接MongoDB
    2、连接Redis
    3、读取MongDB中的分类信息，序列化后，添加到商品爬虫redis_key指定的list
    4、关闭MongoDB
"""
def add_category_to_redis():
    # 1、连接MongoDB
    client = pymongo.MongoClient()
    # 2、连接Redis
    redis_cli = redis.Redis()
    db = client.jd.category
    # 读取分类信息
    corsur = db.find()
    for category in corsur:
        # 3、读取MongDB中的分类信息，序列化后，添加到商品爬虫redis_key指定的list
        data = pickle.dumps(category)
        redis_cli.lpush(JdProductDistributedSpider.redis_key,data)
    # 4、关闭MongoDB
    print('导入成功！')
    client.close()
add_category_to_redis()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
import datetime
class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ArticleLoader(ItemLoader):
    # 自定义TiemLoader
    default_output_processor = TakeFirst()
class ArticleItem(scrapy.Item):
    # 处理数字函数
    def deal_number(value):
        return int(re.findall(r'.*?(\d+).*', value)[0])
    # 转化时间函数
    def date_conver(value):
        try:
            create_date = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
        except Exception as e:
            create_date = datetime.datetime.now()
        return create_date

    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    create_date = scrapy.Field(input_processor=MapCompose(date_conver))
    read_number = scrapy.Field(input_processor=MapCompose(deal_number))
    comment_number = scrapy.Field(input_processor=MapCompose(deal_number))
    content = scrapy.Field()

class PicItem(scrapy.Item):
    pic_url = scrapy.Field()


# 爬取阳光问政平台
class Yangguang(scrapy.Item):
    title = scrapy.Field()
    number_id = scrapy.Field()
    pub_date = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    content = scrapy.Field()


class CfItem(scrapy.Item):

    title = scrapy.Field()
    pub_date = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()

class TiebaItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    img_url = scrapy.Field()

class JdongItem(scrapy.Item):
    b_cate = scrapy.Field()
    s_href = scrapy.Field()
    s_cate = scrapy.Field()
    book_url = scrapy.Field()
    book_img = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_press = scrapy.Field()
    book_pub_date = scrapy.Field()
    book_sku = scrapy.Field()
    book_price = scrapy.Field()

class MyLoader(ItemLoader):
    # 自定义TtemLoader
    default_output_processor = TakeFirst()
class SinaItem(scrapy.Item):
    # 处理数字函数
    def deal_number(value):
        return int(re.match(r'.*?(\d+)', value).group(1))
    # 转化时间函数
    def date_conver(value):
        try:
            create_date = datetime.datetime.strptime(value, "%Y年%m月%日 %H:%M:%S")
        except Exception as e:
            create_date = datetime.datetime.now()
        return create_date

    title = scrapy.Field()
    pub_time = scrapy.Field()
    author = scrapy.Field()
    watch_num = scrapy.Field(
        input_processor=MapCompose(deal_number)
    )
    content = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()

class LagouItem(scrapy.Item):
      title = scrapy.Field()
      url = scrapy.Field()
      url_object_id = scrapy.Field()
      salary = scrapy.Field()
      job_city = scrapy.Field()
      work_years = scrapy.Field()
      degree_need = scrapy.Field()
      job_type = scrapy.Field()
      publish_time = scrapy.Field()
      job_advantage = scrapy.Field()
      job_desc = scrapy.Field()
      job_addr = scrapy.Field()
      company_name = scrapy.Field()
      company_url = scrapy.Field()
      tags = scrapy.Field()
      crawl_time = scrapy.Field()
class ZhenaiItem(scrapy.Item):

    nickname = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
    info = scrapy.Field()
    img_url = scrapy.Field()
    heart = scrapy.Field()
    purple_btns = scrapy.Field()
    pink_btns = scrapy.Field()
    interestion = scrapy.Field()
    condition = scrapy.Field()
class Job51(scrapy.Item):

    title = scrapy.Field()
    money = scrapy.Field()
    company = scrapy.Field()
    msg = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()


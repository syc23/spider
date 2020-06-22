# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    b_category_name = scrapy.Field()
    b_category_url = scrapy.Field()
    m_category_name = scrapy.Field()
    m_category_url = scrapy.Field()
    s_category_name = scrapy.Field()
    s_category_url = scrapy.Field()
class ProductItem(scrapy.Item):
    product_category = scrapy.Field()
    product_sku_id = scrapy.Field()
    product_name = scrapy.Field()
    product_img_url = scrapy.Field()
    product_book_info = scrapy.Field()
    product_option = scrapy.Field()
    product_shop = scrapy.Field()
    product_category_id = scrapy.Field()
    product_comments = scrapy.Field()
    product_ad = scrapy.Field()
    product_price = scrapy.Field()
    shop_url = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    href = scrapy.Field()
    ad_name = scrapy.Field()


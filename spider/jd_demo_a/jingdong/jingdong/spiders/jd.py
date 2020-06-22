# -*- coding: utf-8 -*-
import scrapy
import json
from jingdong.items import CategoryItem
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://dc.3.cn/category/get']

    def parse(self, response):
       result = json.loads(response.body.decode('gbk'))
       item = CategoryItem()
       for data in result['data']:
           b_category = data['s'][0]
           # 大分类信息
           b_category_info = b_category['n']
           item['b_category_name'], item['b_category_url'] = self.getcategory_name_url(b_category_info)
           # print('----------------大分类的名字{}和链接:{}'.format(b_category_name,b_category_url))
           # 中分类列表
           if item['b_category_name']=='美妆':
               m_category_s =  b_category['s']
               for  m_category in  m_category_s:
                   #中分类信息
                   m_category_info = m_category['n']
                   item['m_category_name'],item['m_category_url'] = self.getcategory_name_url(m_category_info)
                   # print('中分类的名称{}和链接:{}'.format(m_category_name,m_category_url))
                   #小分类列表
                   s_category_s = m_category['s']
                   for s_category in s_category_s:
                       # 小分类信息
                       s_category_info = s_category['n']
                       item['s_category_name'], item['s_category_url'] = self.getcategory_name_url(s_category_info)
                       # print('小分类的名称{}和链接:{}'.format(s_category_name,s_category_url))
                       # print(item)
                       # break
                       yield item
           else:
               continue
    def getcategory_name_url(self,category_info):

        category = category_info.split('|')
        category_name = category[1]
        category_url = category[0]
        if category_url.count('jd.com') == 1:
            category_url = 'https://' + category_url
        elif category_url.count('-') == 1:
            category_url = 'https://channel.jd.com/{}.html'.format(category_url)
        else:
            category_url = 'https://list.jd.com/list.html?cat={}'.format(','.join(category_url.split('-')))
        return category_name, category_url

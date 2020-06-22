#!usr/bin/env python  
#-*- coding:utf-8 -*-
from scrapy.cmdline import execute

execute('scrapy crawl jd'.split(' '))
# execute('scrapy crawl jd_product'.split(' '))
# execute('scrapy crawl jd_product_distributed'.split(' '))
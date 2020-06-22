#!usr/bin/env python  
#-*- coding:utf-8 -*-
from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute('scrapy,crawl,blogcto'.split(','))
# execute('scrapy crawl picspider'.split(' '))
# execute('scrapy crawl yangguang'.split(' '))
# execute('scrapy crawl cf'.split(' '))
# execute('scrapy crawl tieba'.split(' '))
# execute('scrapy crawl tt'.split(' '))
# execute('scrapy crawl jd'.split(' '))
# execute('scrapy crawl distribute_jd'.split(' '))
# execute('scrapy crawl renrenspider'.split(' '))
# execute('scrapy crawl jianshu'.split(' '))
execute('scrapy crawl fang'.split(' '))
# execute('scrapy crawl jiaoyou'.split(' '))
# execute('scrapy crawl doubanbook'.split(' '))
# execute('scrapy crawl csdn'.split(' '))
# execute('scrapy crawl lagou'.split(' '))
# execute('scrapy crawl zhenai'.split(' '))
# execute('scrapy crawl ganji'.split(' '))
# execute('scrapy crawl 51job'.split(' '))
# execute('scrapy crawl wangyi'.split(' '))
# execute('scrapy crawl movie_4567kan'.split(' '))
# execute('scrapy crawl qiushi'.split(' '))
# execute('scrapy crawl discovery'.split(' '))
# execute('scrapy crawl maoyan'.split(' '))
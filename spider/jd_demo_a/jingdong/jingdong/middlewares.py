# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import redis
import re
class JingdongSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 实现代理ip中间件
class ProxyMiddleware(object):
    def __init__(self):
        self.redis_cli = redis.Redis()
    def process_request(self, request, spider):
        pass
    def process_exception(self, request, exception, spider):
        data = self.redis_cli.lpop('proxies')
        if data:
            data = data.decode()
            print('处理请求异常，正在使用代理:{}'.format(data))
            if request.url.split(':')[0] == 'http':
                request.meta['proxy'] = 'http://{}'.format(data)
            else:
                request.meta['proxy'] = 'https://{}'.format(data)
            return request
        else:
            pass
# 实现随机请求头中间件
class RandomUserAgent(object):

    def process_request(self, request, spider):
        if request.url.startswith('https://cdnware.m.jd.com'):
           request.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3'
        else:
           request.headers['User-Agent'] = random.choice(spider.settings['USER_AGENT'])
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
import random

class ArticlespiderSpiderMiddleware(object):
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


class ArticlespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
# 设置随机请求头中间件
class RandomUserAgentMidderware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent']= random.choice(spider.settings['USER_AGENT'])

# 设置随机代理中间件
class ProxyMidderware(object):
    # 设置开放代理
    def __init__(self):
        self.proxy_http = [
            'http://94.191.85.55:8080',
        ]
        self.proxy_https = [
            'http://94.191.85.55:8080',
        ]
    # 拦截正常请求
    def process_request(self,request,spider):
        pass
    # 拦截正常响应
    def process_response(self, request, response, spider):
        return response
    # 拦截发生异常的请求对象
    def process_exception(self, request, exception, spider):
        # 当请求发生异常时，启用ip代理，进行访问，
        # 'https://war.163.com/'
        if request.url.split(':')[0]=='http':
            request.meta['proxy'] = random.choice(self.proxy_http)
        else:
            request.meta['proxy'] = random.choice(self.proxy_https)
        # 将修正后的请求对象重新进行请求发送
        return request

        # 设置独享代理 可以这样设置  request.meta['proxy'] = 'https://user:passwd@ip:port'
        # def process_request(self, request, spider):
        #     proxy = 'ip地址：端口号'
        #     user_password = '账号：密码'
        #     request.meta['proxy'] = proxy
        # base64.b64encode需要使用bytes类型
        # import base64
        # b64_user_password = base64.b64encode(user_password.encode('utf-8'))
        # request.headers['Proxy-Authorization'] = 'Basic' + b64_user_password.decode('utf-8')

# selenium+Chrome组合设置请求网页中间件
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse
class SeleniumDownloadMiddersware(object):
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                showmore = self.driver.find_element_by_class_name("show-more")
                showmore.click()
                time.sleep(1)
                if not showmore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response

class Selenium_163_DownloadMiddersware(object):

     def process_request(self, request, spider):
         if request.url in spider.start_urls:
            driver = spider.driver
            driver.get(request.url)
            time.sleep(5)
            try:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(5)
                driver.execute_script('window.scrollTo(0,documnet.body.scrollHeight)')
                time.sleep(5)
                driver.execute_script('window.scrollTo(0,documnet.body.scrollHeight)')
                time.sleep(5)
                driver.execute_script('window.scrollTo(0,documnet.body.scrollHeight)')
            except:
                pass
            time.sleep(10)
            page_text = driver.page_source
            new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
            return new_response

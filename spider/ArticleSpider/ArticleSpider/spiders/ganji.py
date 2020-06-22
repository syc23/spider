# -*- coding: utf-8 -*-
import scrapy
from code_util import ydm
class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['ganji.com']
    start_urls = ['https://passport.ganji.com/login.php?next=/']
    login_url = 'https://passport.ganji.com/login.php'
    code_url = 'https://passport.ganji.com/ajax.php?dir=captcha&module=login_captcha'
    def parse(self, response):
        __hash__ = response.selector.re(r'"__hash__":"(.*?)"')[0]
        yield scrapy.Request(url=self.code_url,callback=self.login,meta={'hashname':'__hash__'})
    def login(self,response):
        __hash__ = response.meta['hashname']
        with open('./code_util/code.png','wb') as f:
            f.write(response.body)
        code = ydm.code('./code_util/code.png')
        data = {
            'username': '18883245172',
            'password': '147258369',
            'setcookie': '14',
            'checkCode':code,
             'next': '/',
            'source': 'passport',
            '__hash__': __hash__
        }
        yield scrapy.FormRequest(url=self.login_url,formdata=data,callback=self.after_login)

    def after_login(self,response):
        print(response.text)
        yield scrapy.Request(url='http://www.ganji.com/vip/account/edit_userinfo.php',callback=self.index)
    def index(self,response):
        with open('./ganji_index.html','w',encoding='utf-8') as f:
            f.write(response.text)

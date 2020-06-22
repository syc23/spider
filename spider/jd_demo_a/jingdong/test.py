#!usr/bin/env python
#-*- coding:utf-8 -*-
# import requests
# import random
# from fake_useragent import FakeUserAgent
# from code_util import ydm
# import parsel
# sess = requests.Session()
# url = 'https://mall.jd.com/showLicence-623261.html'
# headers = {
#     'User-Agent':FakeUserAgent().random
# }
# code_url = 'https://mall.jd.com/sys/vc/createVerifyCode.html?random={}'.format(random.random())
# img_path = './code.jpg'
# contents = sess.get(code_url).content
# with open(img_path, 'wb') as f:
#     f.write(contents)
# code = ydm.code(img_path)
# from_data = {
#     'verifyCode': code
# }
# response = sess.post(url,data=from_data,headers=headers)
# response.encoding = response.apparent_encoding
#
# sel = parsel.Selector(response.text)
# item = {}
# item['name'] = sel.xpath('//div[@class="jScore"]/ul/li[3]/span/text()').extract_first()
# item['position'] = sel.xpath('//div[@class="jScore"]/ul/li[6]/span/text()').extract_first()
# item['href'] = sel.xpath('//div[@class="jScore"]/ul/li[12]/span/a/@href').extract_first()
# print(item)

if '京东' not in '发货地是否会搜个萨嘎撒发大水' :
    print('aaa')

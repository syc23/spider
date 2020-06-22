#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import execjs,json
import jsonpath

class Qiye():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.loginUrl = 'https://vipapi.qimingpian.com/DataList/productListVip'
        self.sess = requests.Session()
    def deal_str(self,un_str):
        js = execjs.compile(open('./deal_qiye_js.js').read())
        return js.call('o',un_str)
    def getcontent(self):
        data = {
            'page': '1',
            'num': '20'
        }
        encrypt_data = self.sess.post(self.loginUrl, data=data, headers=self.headers).json().get('encrypt_data')
        content = self.deal_str(encrypt_data)
        content = json.loads(content)
        self.parse_content(content)
    def parse_content(self,content):
        product = jsonpath.jsonpath(content,'$..product') #项目
        icon = jsonpath.jsonpath(content, '$..icon') #商标
        hangye1 = jsonpath.jsonpath(content, '$..hangye1') #行业领域
        yewu = jsonpath.jsonpath(content, '$..yewu') #业务
        province = jsonpath.jsonpath(content, '$..province') #地区
        lunci = jsonpath.jsonpath(content, '$..lunci') #投资轮次
        jieduan = jsonpath.jsonpath(content, '$..jieduan') #投资阶段
        money = jsonpath.jsonpath(content, '$..money') # 投资金额
        time = jsonpath.jsonpath(content, '$..time') #投资时间
        detail = jsonpath.jsonpath(content, '$..detail') #详情
        heat_num = jsonpath.jsonpath(content, '$..heat_num') #热度
        investors = []
        for i in content['list']:
            investor_list = [tmp for tmp in i['investor_info']]
            investor_str = ','.join([temp.get('investor') for temp in investor_list])
            investors.append(investor_str)
        for _product,_icon,_hangye1,_yewu,_province,_lunci,_jieduan,_money,_time,_detail,_investor,_heat_num in zip(product,icon,hangye1,yewu,province,lunci,jieduan,money,time,detail,investors,heat_num):
            print(_product,_icon,_hangye1,_yewu,_province,_lunci,_jieduan,_money,_time,_detail,_investor,_heat_num)
if __name__ == '__main__':
    qy = Qiye()
    qy.getcontent()
#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import execjs

class Renren():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.getkey_url = 'http://login.renren.com/ajax/getEncryptKey'
        self.login_url = 'http://www.renren.com/ajaxLogin/login'
        self.sess = requests.Session()
        self.pw = '测试密码'
    # 破解密码加密
    def deal_password(self,EncryptKey,pw):
        js = execjs.compile(open('./deal_renren.js').read())
        return js.call('getpasswd',EncryptKey,self.pw)
    def getEncryptKey(self):
        EncryptKey = self.sess.get(self.getkey_url,headers=self.headers).json()
        password = self.deal_password(EncryptKey,self.pw)
        rkey = EncryptKey.get('rkey')
        self.login(password,rkey)
    def login(self,password,rkey):
        data = {
            "email":"测试账号",
            "icode":" ",
            "origURL":"http: //www.renren.com/home",
            "domain":"renren.com",
            "key_id":"1",
            "captcha_type":"web_login",
            "password":password,
            "rkey": rkey,
            "f": " ",
        }
        response = self.sess.post(self.login_url,data=data,headers=self.headers)
        # 进入首页，测试成功登录
        print(self.sess.get("http://www.renren.com/home",headers=self.headers).content.decode('utf-8'))
if __name__ == '__main__':
    renren = Renren()
    renren.getEncryptKey()

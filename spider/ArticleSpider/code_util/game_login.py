#!usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import base64
from code_util.baidu_recognize_code import captcha_recognize
sess  = requests.Session()
url = 'http://ptlogin.4399.com/ptlogin/login.do?v=1'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
content_ = sess.get('http://ptlogin.4399.com/ptlogin/captcha.do?captchaId=captchaReq21effe536e284926025').content
img_path = 'code.jpg'
with open(img_path,'wb') as f:
    f.write(content_)
code = captcha_recognize(img_path)
print(code)
data = {
    'loginFrom':'uframe',
    'postLoginHandler':'default',
    'layoutSelfAdapting':'true',
    'externalLogin':'qq',
    'displayMode':'popup',
    'layout':'vertical',
    'appId':'www_home',
    'gameId':'',
    'css':'',
    'redirectUrl':'',
    'sessionId':'',
    'mainDivId':'popup_login_div',
    'includeFcmInfo':'false',
    'userNameLabel':'4399用户名',
    'userNameTip':'请输入4399用户名',
    'welcomeTip':'欢迎回到4399',
    'sec':'1',
    'password':base64.b64encode('147258369'.encode()).decode(),  # 被坑了,其实就是base64，还以为多复杂，草
    'username':'2087430921',
    'inputCaptcha': code
}
response = sess.post(url,headers=headers,data=data)

html_response = sess.get('http://u.4399.com/user/info',headers=headers)
html_response.encoding = html_response.apparent_encoding
print(html_response.text)
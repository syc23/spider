#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
import json,jsonpath
import hashlib
import time
import base64
class Ip():
    def __init__(self):
        self.timestamp = int(time.time())
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie':'sessionid=tb08ddgthpwy9u5jmbvrrvjqi73bohrt',
        }
    def get_base64_contetn(self,page,num):
        token = hashlib.md5((str(page) + str(num) + str(self.timestamp)).encode('utf-8')).hexdigest()
        url = 'https://nyloner.cn/proxy?page={}&num={}&token={}&t={}'.format(page,num,token,self.timestamp)
        response = requests.get(url,headers=self.headers)
        response.encoding = response.apparent_encoding
        html = json.loads(response.text)
        ip_ports_str = html['list'] if html['list'] else ''
        return ip_ports_str
    def get_true_content(self,page,num):
        """
        base64解密
        scHZjLUh1 = Base64["\x64\x65\x63\x6f\x64\x65"](scHZjLUh1); decode
        key = '\x6e\x79\x6c\x6f\x6e\x65\x72';   nyloner
        len = key["\x6c\x65\x6e\x67\x74\x68"];  length
        code_util = '';
        for (i = 0; i < scHZjLUh1["\x6c\x65\x6e\x67\x74\x68"]; i++) {    length
            var coeFYlqUm2 = i % len;
            code_util += window["\x53\x74\x72\x69\x6e\x67"]["\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65"](scHZjLUh1["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](i) ^ key["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](coeFYlqUm2))
                               String                                  fromCharCode                                                       charCodeAt                                  charCodeAt
        }
        return Base64["\x64\x65\x63\x6f\x64\x65"](code_util)

        """
        scHZjLUh1 = base64.decodebytes(self.get_base64_contetn(page,num).encode())
        key = 'nyloner'
        length = len(key)
        code = ''
        for i in range(len(scHZjLUh1)):
            coeFYlqUm2 = i % length
            code += chr(scHZjLUh1[i]^ ord(key[coeFYlqUm2]))
        code = base64.decodebytes(code.encode()).decode()
        ip_ports = json.loads(code) if code else ''
        for ip_port in ip_ports:
            ip = ip_port['ip']
            port = ip_port['port']
            print(ip,port)

if __name__ == '__main__':
    ip = Ip()

    ip.get_true_content(1,15)
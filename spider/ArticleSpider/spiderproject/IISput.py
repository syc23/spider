#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
from fake_useragent import UserAgent
import sys
import getopt
import threading
import functools
# url = 'http://192.168.0.105'
# headers = {
#     'User-Agent':UserAgent().random
# }
# response = requests.get(url,headers = headers)
# print(response.text)

# url = 'www.baidu.com'
# x = [[1,2,3],[4,5,6],[7,8,9]]
# def test(url,tmp):
#     print(url+':'+str(functools.reduce(lambda x,y:x+y,tmp)))
# thread_list = []
# for i in x:
#     thread_list.append(threading.Thread(target=test,args=(url,i)))
# for i in thread_list:
#     i.start()

import optparse
usage="python -H hostnmae -P port"  #用于显示帮助信息
parser=optparse.OptionParser(usage)  #创建对象实例
parser.add_option('-H',dest='Host',type='string',help='target host',default="127.0.0.1")   ##需要的命令行参数
parser.add_option('-P',dest='Ports',type='string',help='target ports',default="8080")
(options,args)=parser.parse_args()
print(options.Host)
print(options.Ports)

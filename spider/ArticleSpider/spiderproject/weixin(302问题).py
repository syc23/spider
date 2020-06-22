#!usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
from fake_useragent import FakeUserAgent
import parsel
import jsonpath
import re
import time
import csv
from urllib import parse
import random
# 第一个标题 紧急提醒 （68页开始）
# url = 'https://weixin.sogou.com/weixin?query=%E7%B4%A7%E6%80%A5%E6%8F%90%E9%86%92%EF%BC%81%E5%94%AE%E4%BB%B73980%EF%BC%8C%E6%88%90%E6%9C%AC%E4%BB%B780%EF%BC%8C%E4%BD%A0%E8%A2%AB%E5%9D%91%E8%BF%87%E5%90%97%EF%BC%9F&_sug_type_=&s_from=input&_sug_=n&type=2&page=68&ie=utf8'
# 第二个标题 这家70人的小公司让马云坐不住了(第1页开始爬取)
# url = 'https://weixin.sogou.com/weixin?oq=&query=%E8%BF%99%E5%AE%B670%E4%BA%BA%E7%9A%84%E5%B0%8F%E5%85%AC%E5%8F%B8%E8%AE%A9%E9%A9%AC%E4%BA%91%E5%9D%90%E4%B8%8D%E4%BD%8F%E4%BA%86&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=2&_sug_=n&type=2&sst0=1571123105671&page=43&ie=utf8'
# 第三个标题 打起来了！被上海人挤爆到停业的美国Costco，收割了中国哪些人的智商税（重新爬取（第一页开始））
url = 'https://weixin.sogou.com/weixin?oq=&query=%E6%89%93%E8%B5%B7%E6%9D%A5%E4%BA%86%EF%BC%81%E8%A2%AB%E4%B8%8A%E6%B5%B7%E4%BA%BA%E6%8C%A4%E7%88%86%E5%88%B0%E5%81%9C%E4%B8%9A%E7%9A%84%E7%BE%8E%E5%9B%BDCostco%EF%BC%8C%E6%94%B6%E5%89%B2%E4%BA%86%E4%B8%AD%E5%9B%BD%E5%93%AA%E4%BA%9B%E4%BA%BA%E7%9A%84%E6%99%BA%E5%95%86%E7%A8%8E&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=0&_sug_=n&type=2&sst0=1571123303710&page=1&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'
proxy = None
max_count = 5
count = 1
USER_AGENT=[
          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)']
def get_ip():
    headers = {
        'User-Agent':FakeUserAgent().random
    }
    url = 'http://api3.xiguadaili.com/ip/?tid=556756079976571&num=1&category=2&sortby=time&filter=on'
    try:
        response = requests.get(url,headers=headers)
        if response.status_code ==200:
            return response.text
    except Exception as e:
         get_ip()
def get_proxy():
    # url = 'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=c6ab446648a064c98ea290c44a8410f6&orderNo=GL20191015104710SmjfDnA9&count=1&isTxt=0&proxyType=1'
    url = 'http://api.xiaoxiangdaili.com/app/shortProxy/getIp?appKey=501336983676014592&appSecret=YwNcLJ7A&cnt=1&wt=json'
    response = requests.get(url)
    try:
        proxy = str(jsonpath.jsonpath(response.json(), '$..ip')[0]) + ':' + str(jsonpath.jsonpath(response.json(), '$..port')[0])
        return proxy
    except Exception as e:
        return get_proxy()
def get_html(url,count=1):
    print('正在爬取' ,url)
    global proxy
    if count >= max_count:
        print('try too many!')
        return None
    headers = {
        'User-agent':FakeUserAgent().random,
        # 'Cookie':'SUID=A553BC753120910A000000005D579E9B; CXID=43D3BD73396C255D4F0D62E2A30FACD5; ABTEST=0|1570799385|v1; IPLOC=CN5201; weixinIndexVisited=1; SUV=00FF3F47D2280AF15DA07F1AF093F191; JSESSIONID=aaaeDUh4W3WC_hg1on62w; PHPSESSID=ht3i283356j29g4j7js5m9eo92; SNUID=8A7350AB787DECACE9CA67627917514F; sct=15; ppinf=5|1571026592|1572236192|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OiVFNSU5OSVBMnxjcnQ6MTA6MTU3MTAyNjU5MnxyZWZuaWNrOjk6JUU1JTk5JUEyfHVzZXJpZDo0NDpvOXQybHVGdGJ3MXhuMmV3V1hSRENTU3lVejlJQHdlaXhpbi5zb2h1LmNvbXw; pprdig=eWznPWzWx7ILqN6BrKy-ZfGkc_-UGAdVGVMrBOM1HVv_pIZrVt4FTdeV9NbiwhaVQscDogAhXd03jtvUti_Ig6lhpYPzyDNAne_wyOuAuudtkCL_cDCJ_589m57LZuNX-scF1yWVwpjtTkLzRnn-8v1JY72KKUG4xfurSCW6Va4; sgid=01-41643723-AV2j9qDHUXicUUnwUayN4f8o; ppmdig=15710265920000007021a731e5255822c7b8fdfc31eab41d'
    }
    try:
        if proxy:
            print(proxy)
            proxies = {'http':'http://'+proxy}
            response = requests.get(url,headers=headers,proxies=proxies,allow_redirects=False)
        else:
            response = requests.get(url,headers=headers,allow_redirects=False)
        if response.status_code==200:
            response.encoding = response.apparent_encoding
            return response.text
        if response.status_code==302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy',proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except Exception as e:
            print(e)
            proxy = get_proxy()
            count+=1
            return get_html(url,count)
def get_html1(url):
    log = '正在爬取第{}页'.format(count)
    with open('./log.txt', 'a', encoding='utf-8') as f:
        f.write(log +url+'\n')
    print(log)
    headers = {
        # 'User-agent': random.choice(USER_AGENT),
        'User-agent': FakeUserAgent().random,
        # 'Cookie':'SUID=A553BC753120910A000000005D579E9B; CXID=43D3BD73396C255D4F0D62E2A30FACD5; ABTEST=0|1570799385|v1; weixinIndexVisited=1; SUV=00FF3F47D2280AF15DA07F1AF093F191; SNUID=996B4AB36264F68B4FC4D4C9620BAAE7; JSESSIONID=aaaeIO7VN6dpFbkt0Or1w; pgv_pvi=3442375680; pgv_si=s6097819648; IPLOC=CN5200; PHPSESSID=5kf4b1b4nadodal6bqq6i33hq7; sct=28; ppinf=5|1571121825|1572331425|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OiVFNSU5OSVBMnxjcnQ6MTA6MTU3MTEyMTgyNXxyZWZuaWNrOjk6JUU1JTk5JUEyfHVzZXJpZDo0NDpvOXQybHVGdGJ3MXhuMmV3V1hSRENTU3lVejlJQHdlaXhpbi5zb2h1LmNvbXw; pprdig=lNSU0p8_k_81ts_7ftcwBoO929s-mMZ1y68X7ZNwuR9F_V-IbWhMJfWLfAcgMbco_l-PywMeJEya7nloyKubTvvUBzxXYIS92nqXRPuYZqWneCRNq_-1ckgDtRCc8-Phusq4Xn-vCEpqrn_u-lGC5tEZLkOB5Ev6oJtRit04qW8; sgid=01-41643723-AV2laqH199g92jHZhBez6fo; ppmdig=15711218260000003e3302d16cca953cb84620fac0b12bb2'
        'Cookie':'SUID=A553BC753120910A000000005D579E9B; CXID=43D3BD73396C255D4F0D62E2A30FACD5; ABTEST=0|1570799385|v1; weixinIndexVisited=1; SUV=00FF3F47D2280AF15DA07F1AF093F191; IPLOC=CN5201; JSESSIONID=aaa6JFgpvpWLM42NI5s1w; ppinf=5|1571104843|1572314443|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OiVFNSU5OSVBMnxjcnQ6MTA6MTU3MTEwNDg0M3xyZWZuaWNrOjk6JUU1JTk5JUEyfHVzZXJpZDo0NDpvOXQybHVGdGJ3MXhuMmV3V1hSRENTU3lVejlJQHdlaXhpbi5zb2h1LmNvbXw; pprdig=NBAJZcXga_YmqmTh25Dh1GW_gtNkDl-o7FDOxa-rUraCmXVXLXvLq0mqfAv6Qqd40Ic5MQ9xiCw-5C__AFcqHPIYgSkdkLhWiPyJ9dRs8OCepd-5ljMhBFzlLX7Qfgi6w1zEF5L3sK5wKZoqqhR0A5UNPNuEucfyQmMnLgkw8Lg; sgid=01-41643723-AV2lKEtJ7RkRxZuFsapgV8s; PHPSESSID=cd9e6l9l8ecvdo4v60a871rcu0; SNUID=996B4AB36264F68B4FC4D4C9620BAAE7; sct=22; ppmdig=157111096600000005de28951f5fd4d60e1df92d5fa1d9cc'
         }
    # proxy1 = get_proxy()
    proxy1 = get_ip()
    print('正在使用代理ip ',proxy1)
    proxies = {'http': 'http://' + proxy1}
    time.sleep(1)
    try:
        response = requests.get(url,headers=headers,proxies=proxies,timeout=10,allow_redirects=False)
        response.encoding = response.apparent_encoding
        if response.status_code==200:
            print('200','正确解析网页')
            return response.text
        if response.status_code==302:
            print('遇到了302','正在重试中')
            return get_html1(url)
    except Exception as e:
        print('代理连接异常','正在重新请求！',e)
        return get_html1(url)
def get_detail_link(url):
    print('正在爬取详情页',url)
    try:
        content = get_html1(url)
        if content:
            sel = parsel.Selector(content)

            next_page = sel.xpath('//a[@uigs="page_next"]/@href|//a[text()="下一页"]/@href').get()
            li_list = sel.xpath('//ul[@class="news-list"]/li')
            for li in li_list:
                article_link = li.xpath('./div[@class="txt-box"]/h3/a/@data-share').get()
                title = ''.join(li.xpath('./div[@class="txt-box"]/h3/a//text()').getall())
                name = li.xpath('./div[@class="txt-box"]/div[@class="s-p"]/a/text()').get()
                up_time = li.xpath('./div[@class="txt-box"]/div[@class="s-p"]/span//text()').get()
                print(title, name, up_time, article_link)
                with open('weixin3.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([title, name, up_time, article_link])
            if next_page:
                next_page_url = parse.urljoin('https://weixin.sogou.com/weixin', next_page)
                global count
                count += 1
                time.sleep(5)
                get_detail_link(next_page_url)
        else:
            return None
    except Exception as e:
        print(e)
def get_detail(url):
    try:
        content = get_html1(url)
        time.sleep(1)
        title = re.findall(r'<meta property="og:title" content="(.*?)" />',content,re.S)
        title = title[0] if title else ''
        name = re.findall(r'<strong class="profile_nickname">(.*?)</strong>',content,re.S)
        name = name[0]if name else ''
        up_time = re.findall(r'var t="\d+",n="\d+",s="(\d+-\d+-\d+)";',content,re.S)
        up_time = up_time[0] if up_time else ''
        article_link = url
        print(title,name,up_time,article_link)
        # 标题、公众号名称、发文时间、文章链接
        # with open('weixin.txt','a',encoding='utf-8') as f:
        #     line = title+name+up_time+article_link+'\n'
        #     f.write(line)
        with open('weixin1.csv','a',encoding='utf-8',newline='') as f:
             writer = csv.writer(f)
             writer.writerow([title,name,up_time,article_link])
    except Exception as e:
        print(e)
get_detail_link(url)



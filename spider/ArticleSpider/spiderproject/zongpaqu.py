import time
time_start=time.time()
import requests
import re
import parsel
import pymysql
import pymysql.cursors
# db = pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='zuqiu',charset='utf8')
# cursor = db.cursor()
# cursor.execute("drop table if exists qiuyuandata")
# sql="""create table qiuyuandata
# (
#    标号             varchar(100),
#    足球总会         varchar(100),
#    姓名             varchar(100),
#    俱乐部           varchar(100),
#    比分             varchar(100),
#    出场          varchar(100),
#    时间              varchar(100),
#    进球            varchar(100),
#    助攻           varchar(100),
#    射门            varchar(100),
#    射正          varchar(100),
#    黄牌          varchar(100),
#    红牌           varchar(100),
#    犯规            varchar(100),
#    被犯规         varchar(100),
#    扑救             varchar(100),
#    越位            varchar(100),
#    乌龙            varchar(100),
#    点球未进     varchar(100),
#    未失球         varchar(100),
#    primary key (标号,姓名)
# )"""
# cursor.execute(sql)
# db.commit()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
total_page=[24,19,24,20,18]    # 每个总会有的球员的页数
SX=['英超','西甲','意甲','德甲','法甲']
SS=['?search_type=basic_search&keywords=%E8%8B%B1%E8%B6%85&sortField=enName&sort=asc&page=',
    '?search_type=basic_search&keywords=%E8%A5%BF%E7%94%B2&sortField=enName&sort=asc&page=',
    '?search_type=basic_search&keywords=%E6%84%8F%E7%94%B2&sortField=enName&sort=asc&page=',
    '?search_type=basic_search&keywords=%E5%BE%B7%E7%94%B2&sortField=enName&sort=asc&page=',
    '?search_type=basic_search&keywords=%E6%B3%95%E7%94%B2&sortField=enName&sort=asc&page=']

for u in range(4):
    zonghui='https://soccer.hupu.com/g/players/'+SX[u]
# 获取每个总会每个球员的(总会名字,url,名字，俱乐部)
    qiuyuan_info_list = []
    for page in range(1,total_page[u]):
        url_ying=zonghui+SS[u]+str(page)
        response = requests.get(url_ying,headers=headers)
        html = response.text
        all_url = re.findall(r'<li class="left"><a href="(.*?)" target="_blank" title="(.*?)"><img src=.*?</a></li>\n<li .*?俱乐部:&nbsp;<span>(.*?)</span><br />', html)
        all_url = [(SX[u],)+i for i in all_url]
        qiuyuan_info_list=qiuyuan_info_list+all_url

    for add in qiuyuan_info_list:
        url= add[1]     #每个球员信息的url
        print(url)
        response = requests.get(url,headers=headers)
        html = response.text
        sel = parsel.Selector(html)
        infos_list = []
        for tr in sel.xpath('//table[contains(@id,"table_day_data")]//tr[position()>1]')[:-1]:
            info = tr.xpath('./td[position()>4]//text()').getall()
            if info:
                info = [i.replace('\xa0','') for i in info]
                infos_list.append(info)
        infos_list = list(add)+infos_list
        print(infos_list)
# db.close()
time_end=time.time()
print('totally cost',time_end-time_start)

#!usr/bin/env python  
#-*- coding:utf-8 -*-
import redis
import MySQLdb
import json

def process_item():
    # 连接redis数据库
    redis_cli = redis.Redis(host='127.0.0.1',port=6379,db=0)
    #连接mysql数据库
    mysql_cli = MySQLdb.connect(host='localhost',port=3306,user='root',passwd = '147258369',db='spider',charset='utf8')
    # 创建mysql操作游标对象，执行mysql语句
    cursor = mysql_cli.cursor()
    # 将数据从redis数据库中pop出来
    offset = 0
    while True:
        source,data = redis_cli.blpop("distribute_jd:items")
        try:
            if data is not None:
                item = json.loads(data.decode())
                # 创建mysql操作游标对象，执行mysql语句
                cursor = mysql_cli.cursor()
                sql = 'insert into jd(b_cate,s_href,s_cate,book_url,book_img,book_name,book_author,book_press,book_pub_date,book_sku,book_price) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                params = (item['b_cate'],item['s_href'],item['s_cate'],item['book_url'],item['book_img'],item['book_name'],item['book_author'],item['book_press'],item['book_pub_date'],item['book_sku'],item['book_price'])
                cursor.execute(sql, params)
                # 提交事务
                mysql_cli.commit()
                # 关闭游标
                cursor.close()
                offset+=1
                print(offset)
            else:
                print("没有数据了")
                break
        except:
            pass
        

if __name__ == '__main__':
    process_item()
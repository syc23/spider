#!usr/bin/env python  
#-*- coding:utf-8 -*-
import asyncio
import time
"""
    单线程+多任务异步协程
"""
async def request(url):
    # print("正在下载！")
    # 在多任务异步协程实现中，不可以出现不支持异步的相关代码，列如 time.sleep(2)
    # time.sleep(2)
    await asyncio.sleep(2)
    # print("下载完成！")
    return url
def parse(task):
    print(task.result())
loop = asyncio.get_event_loop()

tasks = []
urls = [1,2,3]
for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    task.add_done_callback(parse)
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))

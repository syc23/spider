#!usr/bin/env python  
#-*- coding:utf-8 -*-
import asyncio
import aiohttp
import parsel
import os
import requests
urls = ['https://www.qiushibaike.com/imgrank/page/{}/'.format(i) for i in range(1,14)]

async def parse_html(url):
    async with aiohttp.ClientSession() as res:
        async with await res.get(url) as response:
             html_content = await  response.text()
             sel = parsel.Selector(html_content)
             img_url = ['https:'+url for url in sel.xpath('//div[@class="thumb"]/a/img/@src').extract()]
             return img_url
def get_content(url):
    response = requests.get(url)
    return response.content
def download(task):
    img_urls = task.result()
    for url in img_urls:
        print('正在下载{}'.format(url))
        filename = os.path.join('./img/',os.path.basename(url))
        with open(filename,'wb') as f:
            f.write(get_content(url))

tasks = []
for url in urls:
    c = parse_html(url)
    task = asyncio.ensure_future(c)
    task.add_done_callback(download)
    tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))


#!usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
import parsel
from fake_useragent import UserAgent
import re
from urllib import parse

class Ziroom():
    def __init__(self):
        self.headers = {
        'User-Agent':UserAgent().random
        }
        self.base_url = 'http://sh.ziroom.com/z/p{}/'
        self.sess = requests.Session()
    def getcontent(self,url):
        response = self.sess.get(url, headers=self.headers)
        response.encoding = response.apparent_encoding
        content = response.text
        return content

    def recon_img(self,content):
        """
        1、获取图片
        2、调用训练好的模型识别图像中的数字
        :return:
        """
        img_url = re.findall(r'url\((.*?)\)',content)
        if img_url:
            img_url,*_ = img_url
            img_url = parse.urljoin('https:',img_url)
            # 保存，识别
            with open('./code_img/code.png','wb') as f:
                f.write(self.sess.get(img_url).content)
        #     调用预训练模型识别
        #     model = model()
        #     img = np.array(Image.open('./code_img/code.png'))
        #     img = np.expand_dims(img,axis=-1)
        #     pred = model.predict(img)
        #     pred_digest = pred.argmax(axis=-1)
        #     print(pred_digest)
        #     return value
        pass


    def get_map(self,ss):
        digest = ss
        pxs = ['-0px','-21.4px','-42.8px','-64.2px','-85.6px','-107px','-128.4px','-149.8px','-171.2px','-192.6px']
        pxtovalue = dict(zip(pxs,digest))
        return pxtovalue

    def get_detail(self,content):
        ss = self.recon_img(content) # 识别数字，返回字符串
        sel = parsel.Selector(content)
        pxstovalue = self.get_map(ss) # 将字符串和pxs组成key-value 如{px:2}
        for div in sel.xpath('//div[@class="Z_list-box"]/div'):
            px_list = div.xpath('./div[@class="info-box"]/div[@class="price"]//span[@class="num"]/@style').getall()
            if px_list:
                pxs = [i.split(':')[-1].strip() for i in px_list] # 得到pxs
                price = ''.join([pxstovalue[i] for i in pxs]) # pxs转 数字
                print(price)

    def start(self):
        urls = [self.base_url.format(i) for i in range(51)]
        for url in urls:
            content = self.getcontent(url)
            self.get_detail(content)
            break

headers = {
        'User-Agent':UserAgent().random
        }
def getcontent(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    content = response.text
    return content
def recon_img(content,i):
    img_url = re.findall(r'url\((.*?)\)',content)
    if img_url:
        img_url,*_ = img_url
        img_url = parse.urljoin('https:',img_url)
        print(img_url)
        # 保存，识别
        with open(r'C:\Users\acer\Desktop\DataAnalysis\pytorch_study\CNN_captha\train\{}.png'.format(i),'wb') as f:
            f.write(requests.get(img_url).content)
if __name__ == '__main__':
    # ziroom = Ziroom()
    # ziroom.start()
    url_list = ['http://hz.ziroom.com/z/p{}/'.format(i) for i in range(1,51)]
    for idx,i in enumerate(url_list):
        content = getcontent(i)
        recon_img(content,idx)

    pass





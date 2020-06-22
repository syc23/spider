#!usr/bin/env python  
#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import jieba,re
from wordcloud import WordCloud,ImageColorGenerator
# from scipy.misc import imread
data = open('./title.txt','r',encoding='utf-8').read()
data = re.sub(r'&nbsp;','',data)
result = ' '.join(jieba.cut(data))
# img = imread('./11.jpg')
wc = WordCloud(
    font_path=r'./simsun.ttc',
    min_font_size=10,
    max_font_size=50,
    width=500,
    height=350,
    background_color='white',
    # mask=img,
)
wc.generate(result)
# 从背景里面提取背景颜色
# image_color = ImageColorGenerator(img)
# wc.recolor(color_func=image_color)
plt.figure('wordcloud',figsize=(10,8))
mp = plt.get_current_fig_manager()
mp.window.wm_geometry('+440+110')
plt.axis('off')
plt.imshow(wc)
plt.savefig('./title.jpg')
plt.show()

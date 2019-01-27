# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 11:41:42 2019

@author: Windows User
"""

from requests_html import HTMLSession
session = HTMLSession()
url = 'https://www.jianshu.com/p/85f4624485b9'
r = session.get(url)

#把服务器传回来的内容当作HTML文件类型处理，只看文字部分。
print(r.html.text)

r.html.links#包括针对所在域名的相对连接
r.html.absolute_links

#HTML是一种标记语言（超文本标记语言，HyperText Markup Language）
#右键-检查
#对这个函数，给定一个选择路径（sel），返回所有描述文本和链接路径
def get_text_link_from_sel(sel):
    mylist = []
    try:
        results = r.html.find(sel)
        for result in results:
            mytext = result.text
            mylink = list(result.absolute_links)[0]
            mylist.append((mytext, mylink))
        return mylist
    except:
        return None
 
sel1='body > div.note > div.post > div.article > div.show-content > div > p:nth-child(4) > a'
get_text_link_from_sel(sel1)

sel_all='body > div.note > div.post > div.article > div.show-content > div > p > a'
get_text_link_from_sel(sel_all)

import pandas as pd
df=pd.DataFrame(get_text_link_from_sel(sel_all))
df.columns = ['text', 'link']


df.to_csv('output.csv', encoding='gbk', index=False)
#注意这里需要指定encoding（编码）为gbk，否则默认的utf-8编码在Excel中查看的时候，有可能是乱码。










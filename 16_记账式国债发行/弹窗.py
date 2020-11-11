# coding:utf-8
# 1. 获得网页内容
# 2. 建立数据库，先仅仅获取第一条内容
# 3. 对比，有差异进行发送邮件

import requests
from bs4 import BeautifulSoup
import time,datetime
from detail import get_detail
import webbrowser


def get_url():
    url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/'
    res=requests.get(url)
    text=res.content
    # with open('main.html','wb') as f:
    #     f.write(text)
    #     f.close()
    soup=BeautifulSoup(text,'lxml')
    info_list=soup.find_all('ul',class_='liBox')[0]
    # 获取单个的数据，目前先只考虑第一个
    for one in info_list.find_all('li'):
        title=one.text
        date=one.span.text
        href=url+one.a.attrs['href'][2:]
        return [title,date,href]


import win32api,win32con


init_info=get_url()
details=get_detail(init_info[2])
title,the_url=init_info[0],init_info[2]
print('目前最新:',title)
webbrowser.open(the_url)
win32api.MessageBox(0, details, title, win32con.MB_ICONWARNING)

while True:
    info=get_url()
    if info!=init_info:
        print('有新消息：{}'.format(info[0]))
        details=get_detail(info[2])
        title,the_url = info[0],info[2]
        # 新消息提醒方式
        webbrowser.open(the_url)
        win32api.MessageBox(0, details,title, win32con.MB_ICONWARNING)

    else:
        print('\r{} 无变化'.format(datetime.datetime.now()),end='')
    time.sleep(10)
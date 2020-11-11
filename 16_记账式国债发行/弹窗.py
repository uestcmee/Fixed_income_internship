# coding:utf-8
# 1. 获得网页内容
# 2. 建立数据库，先仅仅获取第一条内容
# 3. 对比，有差异进行警告

import requests
from bs4 import BeautifulSoup
import time,datetime
from detail import get_detail
import webbrowser
import win32api,win32con


def get_url():
    url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/'
    res=requests.get(url)
    text=res.content
    soup=BeautifulSoup(text,'lxml')
    info_list=soup.find_all('ul',class_='liBox')[0]
    # 获取单个的数据，目前考虑前五个
    tot_list=[]
    for one in info_list.find_all('li')[:5]:
        title=one.text
        date=one.span.text
        href=url+one.a.attrs['href'][2:]
        tot_list.append([title, date, href])
    return tot_list


def alert(title,details,the_url):
    webbrowser.open(the_url) # 打开浏览器
    win32api.MessageBox(0, details, title, win32con.MB_ICONWARNING|win32con.MB_SYSTEMMODAL) # 弹窗提示


info_0=get_url()
title=info_0[0][0] # 第一条的标题
print('目前最新:',title)
# alert('初始测试',title,'http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/')

while True:
    info_now=get_url()
    if info_now!=info_0: # 有差异
        change_num = info_now.index(info_0[0]) # 新的里面找原有的在第几位
        print('有{}条新消息'.format(change_num))
        for i in range(change_num):
            title='第({}/{})个新消息：{}'.format(i+1,change_num,info_now[i][0])
            details = get_detail(info_now[i][2])
            the_url = info_now[i][2]
            print(title)
            # 新消息提醒
            alert(title, details=details, the_url=the_url)

        info_0=info_now # 更新现有list

    else:
        now_time = str(datetime.datetime.now())[:19]
        for i in range(5,0,-1):
            print('\r{} 无变化    {}s后再次获取'.format(now_time,i),end='')
            time.sleep(1)
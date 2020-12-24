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
import traceback # 不用这个，输出太多了
import threading,re

def get_url():
    url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/'
    res=requests.get(url)
    text=res.content
    soup=BeautifulSoup(text,'lxml')
    info_list=soup.find_all('ul',class_='liBox')[0]
    # 获取单个的数据，目前考虑前五个
    tot_list=[]
    for one in info_list.find_all('li')[:10]:
        title=one.text
        date=one.span.text
        href=url+one.a.attrs['href'][2:]
        if title[:6]=='国债业务公告':
            continue
        tot_list.append([title, date, href])
    return tot_list


def alert(title,details,the_url=''):
    if the_url=='':
        pass
    elif isinstance(the_url,str):
        webbrowser.open(the_url) # 打开浏览器
    elif isinstance(the_url, list):
        for url in the_url:
            webbrowser.open(url)  # 打开浏览器
    win32api.MessageBox(0, details, title, win32con.MB_ICONWARNING|win32con.MB_SYSTEMMODAL) # 弹窗提示


info_0=get_url()
title=info_0[0][0] # 第一条的标题
# print('目前最新:',title)
for i in info_0:
    print (i[0])

# alert('初始测试',title,'http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/')

while True:
    try:
        info_now=get_url() # 新的信息列表
        if info_now!=info_0: # 有差异
            change_num = info_now.index(info_0[0]) # 新的里面找原有的在第几位
            print('有{}条新消息'.format(change_num))
            amount_term=[]
            for i in range(change_num):
                head='共有{}个新消息'.format(change_num)
                details = get_detail(info_now[i][2])

                term = re.findall('\d+年期|(?<=期限)\d+天', details)[0]  # 期限
                amount = re.findall('(总额\d+亿元)',details)[0]
                title=info_now[i][0]
                amount_term.append('{}\n\n===>{}<===\n===>{}<===\n\n'.format(title,term,amount))

                url=info_now[i][2]
                webbrowser.open(url)  # 打开浏览器

            # 新消息提醒
            remind_info='\n'.join(amount_term)
            alert(head,details=remind_info)
                # alert(title, details=details, the_url=the_url)

            info_0=info_now # 更新现有list
            time.sleep(50)
        else:
            now_time = str(datetime.datetime.now())[:19]
            for i in range(5,0,-1):
                print('\r{} 无变化    {}s后再次获取'.format(now_time,i),end='')
                time.sleep(1)
    except Exception as e:
        now_time = str(datetime.datetime.now())[:19]
        traceback.print_exc()
        for i in range(5, 0, -1):
            print('\r{} 出现问题{}    {}s后再次获取'.format(now_time,e, i), end='')
            time.sleep(1)
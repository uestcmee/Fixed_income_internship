# coding:utf-8
# 1. 获得网页内容
# 2. 建立数据库，先仅仅获取第一条内容
# 3. 对比，有差异进行警告

import requests
from bs4 import BeautifulSoup
import time,datetime
from detail import get_detail
import webbrowser
import traceback # 不用这个，输出太多了
import re
import threading

from tkinter import *
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
    window = Tk()
    # 2.配置这个窗口（window）的响应参数
    window.title(title)
    # window.geometry("200x200")
    window.resizable(0, 0)  # 设置窗口大小不可变

    Label(window,text='名称') .grid(row=0,column=0,columnspan=5)
    Label(window,text='发行期限',width=10) .grid(row=0,column=5)
    Label(window,text='发行量') .grid(row=0,column=6)
    name=Listbox(window,width=55, height=5)
    name.grid(row=1,column=0,columnspan=5,rowspan=5)

    term_list=Listbox(window,width=10, height=5)
    term_list.grid(row=1,column=5,rowspan=5,sticky=S)

    amount_list=Listbox(window,width=10, height=5)
    amount_list.grid(row=1,column=6,rowspan=5)
    for one in details:
        name.insert(END,one[0][8:-10])
        term_list.insert(END,one[1])
        amount_list.insert(END,one[2])

    # 运行窗口
    window.mainloop()


# 主要对比函数，需要传入对比基准
def main_fun(info_0):

    try:
        info_now = get_url()  # 新的信息列表
        if info_now != info_0:  # 有差异
            change_num = info_now.index(info_0[0])  # 新的里面找原有的在第几位
            print('有{}条新消息'.format(change_num))
            amount_term = []
            for i in range(change_num):
                details = get_detail(info_now[i][2])

                term = re.findall('(\d+年期)', details)[0]
                amount = re.findall('(总额\d+亿元)', details)[0]
                title = info_now[i][0]
                amount_term.append([title, term, amount])
                url = info_now[i][2]
                webbrowser.open(url)  # 打开浏览器

            # 新消息提醒
            head = '共有{}个国债发行'.format(change_num)
            # 多线程方式弹窗，避免阻塞后续信息
            t = threading.Thread(target=alert, args=(head, details,))
            # alert(head,details=amount_term)
            t.start()

            info_0 = info_now  # 更新现有list

            info_0=main_fun(info_0) # 直接递归取消延时
            return info_0 # 递归结束后，确保返回一个最新值

        else:
            # 无变化
            return info_0

    except Exception as e:
        # now_time = str(datetime.datetime.now())[:19]
        # for i in range(5, 0, -1):
        #     print('\r{} 出现问题{}    {}s后再次获取'.format(now_time, e, i), end='')
        #     time.sleep(1)
        print('获取出现问题')
        return info_0


# 如果直接运行该文件，进入无限循环
if __name__ == '__main__':
    info_0 = get_url()
    title = info_0[0][0]  # 第一条的标题
    # print('目前最新:',title)
    for i in info_0:
        print(i[0])
    while True:

        info_0=main_fun(info_0) # 主函数，更新比较基准
        # 延时5s ,延时放外面只用写一个函数，但是要传参
        for i in range(5, 0, -1):# 延时
            now_time = str(datetime.datetime.now())[:19]
            print('\r {}s后再次获取  {}'.format(i,now_time), end='')
            time.sleep(1)
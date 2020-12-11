# coding:utf-8
# 1. 获得网页内容
# 2. 建立数据库，先仅仅获取第一条内容
# 3. 对比，有差异进行警告
# 断网处理一定要做，刚开机可能没联网

import requests
from bs4 import BeautifulSoup
import time,datetime
import webbrowser
import threading
import gc
# import traceback # 不用这个，输出太多了
# import re

from tkinter import *


class BondRemind:
    def __init__(self):
        self.info_0 = self.get_url()
        if self.info_0!=[]:
            print(str(datetime.datetime.now().time())[:8])
            for i in self.info_0:
                print(i[0])

    def get_detail(self,url):
        """
        获取详情页面的页面内容
        :param url: 网页url
        :return:
        """
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        detail = soup.find('div', class_='my_conboxzw')
        return detail.text

    def get_url(self):
        """
        获取列表页的页面内容
        :return:
        """
        url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/'
        try:
            res=requests.get(url)
            # if hasattr(self,'my_th'):
            #     self.my_th.
        except Exception as e :
            # print(e)
            print('无法获得页面内容')
            if not hasattr(self,'my_th'):
                self.my_th=threading.Thread(target=self.alert,args=('无法更新内容',[['无法更新列表，请检查网页链接','','']],))
                # self.alert('无法更新内容',details=['无法更新列表，请检查网页链接',])
                self.my_th.start()
            return []
        text=res.content
        soup=BeautifulSoup(text,'lxml')
        info_list=soup.find_all('ul',class_='liBox')[0]
        # 获取单个的数据，目前考虑前10个
        tot_list=[]
        for one in info_list.find_all('li')[:10]:
            title=one.text
            date=one.span.text
            href=url+one.a.attrs['href'][2:]
            if title[:6]=='国债业务公告':
                continue
            tot_list.append([title, date, href])
        return tot_list

    def alert(self,title,details:list,the_url=''):
        """
        一次更新表格，不用动态更改参数
        :param title:
        :param details:
        :param the_url:
        :return:
        """
        print(threading.current_thread())
        assert len(details)>0 and len(details[0])==3,'传入的列表有误'
        window = Tk()
        # 2.配置这个窗口（window）的响应参数
        window.title(title)
        window.resizable(0, 0)  # 设置窗口大小不可变
        # 标签
        Label(window,text='名称') .grid(row=0,column=0,columnspan=5)
        Label(window,text='发行期限',width=10) .grid(row=0,column=5)
        Label(window,text='发行量') .grid(row=0,column=6)
        # 公告名
        name=Listbox(window,width=55, height=5)
        name.grid(row=1,column=0,columnspan=5,rowspan=5)
        # 公告期限
        term_list=Listbox(window,width=10, height=5)
        term_list.grid(row=1,column=5,rowspan=5,sticky=S)
        # 公告发行量
        amount_list=Listbox(window,width=10, height=5)
        amount_list.grid(row=1,column=6,rowspan=5)
        for one in details:
            name.insert(END,one[0])
            term_list.insert(END,one[1])
            amount_list.insert(END,one[2])
        # 运行窗口
        window.mainloop()
        window.quit()
        # gc.collect()
        delattr(self,'my_th')

    def new_msg_process(self,info_now):
        change_num = info_now.index(self.info_0[0])  # 新的里面找原有的在第几位
        print('有{}条新消息'.format(change_num))
        amount_term = []
        for i in range(change_num):
            details = self.get_detail(info_now[i][2]) # 获取网页详情

            term = re.findall('(\d+年期)', details)[0] # 期限
            amount = re.findall('(总额\d+亿元)', details)[0] # 发行量
            title = info_now[i][0][8:-10] # 标题

            amount_term.append([title, term, amount])
            url = info_now[i][2]
            webbrowser.open(url)  # 打开浏览器

        # 新消息提醒
        head = '共有{}个国债发行'.format(change_num)
        # 多线程方式弹窗，避免阻塞后续信息
        t = threading.Thread(target=self.alert, args=(head, amount_term,))
        t.start()

    # 主要对比函数，需要传入对比基准
    def main_fun(self):
        try:
            info_now = self.get_url()  # 新的信息列表
            if info_now==[]:
                print('无法更新公告列表')
                return 1
            if info_now != self.info_0:  # 有差异

                self.new_msg_process(info_now) # 此处对差异进行处理

                self.info_0 = info_now  # 更新现有list
                self.main_fun() # 直接递归取消延时
            else:
                # 无变化
                pass
        except Exception as e:
            print('获取出现问题')
            pass


# 如果直接运行该文件，进入无限循环
if __name__ == '__main__':
    br=BondRemind()
    while True:
        br.main_fun()
        for i in range(5, 0, -1):  # 延时
            now_time = str(datetime.datetime.now())[:19]
            print('\r {}s后再次获取  {}'.format(i, now_time), end='')
            time.sleep(1)


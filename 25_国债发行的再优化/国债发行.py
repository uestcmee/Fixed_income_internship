# coding:utf-8
# 1. 获得网页内容
# 2. 建立数据库，先仅仅获取第一条内容
# 3. 对比，有差异进行警告
# 断网处理一定要做，刚开机可能没联网
# 点击关闭按钮就直接退出了！

import requests
from bs4 import BeautifulSoup
import time,datetime
import webbrowser
import threading
# import win32api,win32con
# 设置python exe运行时不显示窗口
import win32api, win32gui
ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0,ct)
win32gui.ShowWindow(hd,0)
import sys
import gc
import traceback # 不用这个，输出太多了
# import re

import tkinter.messagebox
from tkinter import *


class BondRemind:
    def __init__(self):
        """
        初始化程序
        """
        # 打开界面
        init_t = threading.Thread(target=self.alert, args=('国债发行检测',))
        init_t.start()
        self.window_opend = True
        self.info_0 = self.get_url()
        self.new_msg_process(info_now=self.info_0,init=True) # 初始数据传入界面
        print(str(datetime.datetime.now().time())[:8])
        for i in self.info_0:
            print(i[0]) # 输出新的消息

    def restore(self):
        """
        重置文字
        :return:
        """
        for box in ['name', 'term', 'amount','date']:
            self.window_info[box].delete(0,END)
        info_0 = self.get_url()
        self.new_msg_process(info_now=info_0,init=True) # 初始数据传入界面


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
            print('无法获得页面内容')
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

    def alert(self,title,the_url=''):
        """
        动态更改参数
        :param title:
        :param details:
        :param the_url:
        :return:
        """
        print(threading.current_thread())
        # 调用该函数用于初始化，不传入detail
        # assert len(details)>0 and len(details[0])==3,'传入的列表有误'
        window = Tk()
        # 2.配置这个窗口（window）的响应参数
        window.title(title)
        window.resizable(0, 0)  # 设置窗口大小不可变
        # 标签
        # Label(window,text='名称') .grid(row=0,column=4,columnspan=1)
        Label(window,text='发行期限',width=10) .grid(row=0,column=5)
        Label(window,text='发行量') .grid(row=0,column=6)
        Label(window,text='日期') .grid(row=0,column=7)

        Button(window,text='测试',command=lambda :self.main_fun(True),width=10).grid(row=0,column=2,sticky=W)
        Button(window,text='重置',command=lambda :self.restore(),width=10).grid(row=0,column=3,sticky=W)
        Button(window,text='网址',command=lambda :self.open_main_url(),width=10).grid(row=0,column=4,sticky=W)

        # 时间框
        time_box=Listbox(window,height=1)
        time_box.grid(row=0,column=0,columnspan=2,sticky=W)

        # 公告名
        name=Listbox(window,width=55, height=7)
        name.grid(row=1,column=0,columnspan=5,rowspan=5)
        # 公告期限
        term_list=Listbox(window,width=10, height=7)
        term_list.grid(row=1,column=5,rowspan=5,sticky=S)
        # 公告发行量
        amount_list=Listbox(window,width=10, height=7)
        amount_list.grid(row=1,column=6,rowspan=5)
        # 公告日期
        date=Listbox(window,width=10, height=7)
        date.grid(row=1,column=7,rowspan=5)

        # 运行窗口
        self.window_info={
            'window':window,
            'time_box':time_box,
            'name':name,
            'term':term_list,
            'amount':amount_list,
            'date': date

        }
        window.protocol('WM_DELETE_WINDOW', self.exit)
        window.mainloop()
        # 由于关闭使用exit函数，下面的这些好像也用不到，也不涉及gc来回收变量的问题
        # window.quit()
        # self.window_opend = False
        #
        # delattr(self,'window_info')# 删除对应变量
        # gc.collect()
        # print('关闭完成')


    def insert_info(self,info:list,color=None):
        """
        用来写入界面内容，传入list
        :param info:
        :param color:
        :return:
        """
        self.window_info['name'].insert(0, info[0])
        self.window_info['term'].insert(0, info[1])
        self.window_info['amount'].insert(0, info[2])
        self.window_info['date'].insert(0, info[3])
        if color:
            self.window_info['name'].itemconfig(0, {'bg': color})
        return 0

    def exit(self):
        quit = tkinter.messagebox.askokcancel('提示', '真的要退出吗？')
        if quit == True:
            self.window_info['window'].quit()
            self.window_opend = False

            # sys.exit()
        else:
            pass
    def open_main_url(self):
        url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/'
        webbrowser.open(url)
        return 0

    def new_msg_process(self,info_now,init=False):
        error_notice='获取内容失败，请检查网络连接'
        if info_now == []:
            if self.window_info['name'].get(0) != error_notice:
                print('无法更新公告列表')
                self.insert_info([error_notice,' ',' ',' '] , color = '#F00056')

            return 1

        if info_now != [] and self.window_info['name'].get(0) == error_notice:
            self.insert_info(['已恢复连接', ' ', ' ', ' '], color='#90EE90')

            if self.window_info['name'].get(2) == '':  # 一开界面的时候就断网的情况
                self.info_0 = self.get_url()
                if self.info_0 != []:
                    self.new_msg_process(info_now=self.info_0, init=True)  # 初始数据传入界面
                    print(str(datetime.datetime.now().time())[:8])
                    for i in self.info_0:
                        print(i[0])

        if init: # 如果是初始化
            change_num=len(info_now)
        else:
            change_num = info_now.index(self.info_0[0])  # 新的里面找原有的在第几位
        print('有{}条新消息'.format(change_num))
        amount_term = []

        for i in range(change_num):
            details = self.get_detail(info_now[i][2]) # 获取网页详情
            # print(info_now[i][2]) # 打印url
            term = re.findall('\d+年期|(?<=期限)\d+天', details)[0] # 期限
            term=str(term).replace('{}','')
            amount = re.findall('(?<=总额)(\d+亿元)', details)[0] # 发行量
            title = info_now[i][0][8:-10] # 标题
            date = info_now[i][0][-10:] # 公告发布日期

            amount_term.append([title, term, amount,date])
            url = info_now[i][2]
            if not init: # 如果不是初始化
                webbrowser.open(url)  # 打开浏览器
        # 新消息提醒
        if not init :
            self.window_info['window'].wm_attributes('-topmost',1)# 置顶显示
        for one in amount_term[::-1]: # 换向，以便按顺序插入
            self.insert_info(one)
            if not init:
                for box in ['name','term','amount','date']:
                    self.window_info[box].itemconfig(0, {'bg': '#FF4D00'})

    # 主要对比函数，需要传入对比基准
    def main_fun(self,test=False):
        try:
            if self.window_opend == False:
                sys.exit(-1)

            info_now = self.get_url()  # 新的信息列表
            # 更新界面
            datet = str(datetime.datetime.now())[:19]
            # 更新时间
            self.window_info['time_box'].delete(END)
            self.window_info['time_box'].insert(END, datet)

            if test:#  调试修改此处，假装有新的
                info_now[2]=info_now[0]
                info_now[0]=info_now[1]

            if info_now != self.info_0:  # 有差异

                self.new_msg_process(info_now) # 此处对差异进行处理
                self.info_0 = info_now  # 更新现有list
                # self.main_fun() # 直接递归取消延时

            else:
                self.window_info['window'].wm_attributes('-topmost', 0)  # 置顶显示
                # 无变化
                pass
        except Exception as e:
            traceback.print_exc()
            print('获取出现问题',e)
            pass


# 如果直接运行该文件，进入无限循环
if __name__ == '__main__':
    br=BondRemind()
    while True:
        br.main_fun()
        for i in range(9, 0, -1):  # 延时
            now_time = str(datetime.datetime.now())[:19]
            print('\r {}s后再次获取  {}'.format(i/10, now_time[11:]), end='')
            time.sleep(0.1)


# 定期获取数据，定时模块单独封装
# 后期可以使用mainloop文件进行定时
import datetime
import time,os
import tkinter as tk
import threading
import gc
from tkinter import *
from tkinter.filedialog import (askopenfilename)



def main_window():
    print(threading.current_thread())
    # 调用该函数用于初始化，不传入detail

    window = Tk()
    # 2.配置这个窗口（window）的响应参数
    window.title('定时启动设置')
    window.resizable(0, 0)  # 设置窗口大小不可变
    # 标签
    # Label(window,text='名称') .grid(row=0,column=4,columnspan=1)
    Label(window, text='发行期限', width=10).grid(row=0, column=5)
    Label(window, text='发行量').grid(row=0, column=6)
    Label(window, text='日期').grid(row=0, column=7)

    Button(window, text='测试', command= askopenfilename, width=10).grid(row=0, column=2, sticky=W)
    # Button(window, text='重置', command=lambda: self.restore(), width=10).grid(row=0, column=3, sticky=W)

    # 时间框
    time_box = Listbox(window, height=1)
    time_box.grid(row=0, column=0, columnspan=2, sticky=W)

    # 公告名
    name = Listbox(window, width=55, height=7)
    name.grid(row=1, column=0, columnspan=5, rowspan=5)
    # 公告期限
    term_list = Listbox(window, width=10, height=7)
    term_list.grid(row=1, column=5, rowspan=5, sticky=S)
    # 公告发行量
    amount_list = Listbox(window, width=10, height=7)
    amount_list.grid(row=1, column=6, rowspan=5)
    # 公告日期
    date = Listbox(window, width=10, height=7)
    date.grid(row=1, column=7, rowspan=5)

    # 运行窗口
    # self.window_info = {
    #     'window': window,
    #     'time_box': time_box,
    #     'name': name,
    #     'term': term_list,
    #     'amount': amount_list,
    #     'date': date
    #
    # }
    window.mainloop()
    # window.quit()
    # delattr(self, 'window_info')  # 删除对应变量
    # gc.collect()
    # print('关闭完成')
    # self.window_opend = False


# from timed_start import Timing

if __name__ == '__main__':
    print('成交数据每日爬虫')
    main_window()



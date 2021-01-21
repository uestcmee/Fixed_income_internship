# 定期获取数据，定时模块单独封装
# 后期可以使用mainloop文件进行定时
# 其实相比于现有的定时函数，感觉优势是，可以在一段时间内检测到符合时间标准后都可以运行
# 但是带来的问题就是如果不采用定制的tkinter提醒的话,就会一直弹窗（tkinter关闭后可检测关闭然后不再提示）
# 且国债发行还需要整段时间的监控
# 解决方案：等待中就不要提醒了！

import datetime
import time,os
import tkinter as tk
import threading
import gc
from win10toast import ToastNotifier
# 获取债券数据


class Timing:
    def __init__(self,title:str='同业成交爬虫',rule:str='weekday==3 and hour>9 and hour <=18'):
        self.no_need_window = False
        self.title=title
        self.rule=rule
        self.toaster = ToastNotifier()
        self.show_notifier(title,'开始运行')

    def show_notifier(self,title,text=':)'):
        self.toaster.show_toast(title,
                           text,
                           # icon_path="涨跌.ico",
                           duration=5)
        return 0

    def sleep(self,wait_time:int):
        """
        休眠函数，每一秒刷新一次
        :param wait_time: 休眠时间（s)
        :return:
        """
        for i in range(wait_time, 0, -1):  # 延时
            now_time = str(datetime.datetime.now())[:19]
            print('\r{}s后再次获取  {}'.format(i, now_time), end='')
            time.sleep(1)


    def main_loop(self,func,wait_time=5):
        """
        :param func: 所需要唤醒的函数
        :param rule: 使用的规则，以字符串形式
        :return: 无返回
        """
        while True: # 定时启动
            """ 更新时间区"""
            date_time = datetime.datetime.today()
            weekday = date_time.weekday()
            date=date_time.date()
            tim= str(date_time.time())[:8]# 为了方便传入使用的时间格式

            """时间判断区"""
            if eval(self.rule) :    # 规定的时间
                # self.show_notifier('开始运行')
                '''函数在这里！！！'''
                func()
                '''函数在这里！！！'''
                # self.show_notifier('已运行完成')
                # 延时5s
                self.sleep(wait_time)
            else: # 非所需时间
                print('  时间未到'.format(date_time),end='')
                self.sleep(wait_time) # 延时1s


if __name__ == '__main__':
    print('成交数据每日爬虫')
    # 工作日获取债券信息
    def fake_func():
        print('hello')
    Timing(rule='weekday<5 and tim>"20:11:00"').main_loop(func=fake_func,wait_time=1)
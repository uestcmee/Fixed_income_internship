# 定期获取数据，定时模块单独封装
# 后期可以使用mainloop文件进行定时
import datetime
import time,os
import tkinter as tk
import threading
import gc
# from mttkinter import mtTkinter as tk

# 获取债券数据
def fetch_bond_info():
    """
    获取债券数据的文件，如果文件已经存在，则跳过
    :return:
    """
    date_time = datetime.datetime.today()
    date = date_time.date()

    exist_flag = ('债券成交{}.csv'.format(date)) in os.listdir('./csv')
    if exist_flag: # 已经存在
        print('今日结果已经存在')
        # time.sleep(300)# 延时五分钟
        return 0
    else:
        print('获取今日成交')
        if ('ak' not in locals()): # 避免重复import
            import akshare as ak
        bond_df_raw = ak.bond_spot_deal()
        bond_df_raw.to_csv('./csv/债券成交{}.csv'.format(date),encoding='gbk')
        print('成交获取完成')
        th = threading.Thread(target=msg_box, args=(date,))
        th.start()
        return 0

# 弹窗提示获取完成，开新的线程调用
def msg_box(date):
    """
    子函数所使用的弹窗，非必须
    :param date: 日期，此处为了命名文件
    :return: 无
    """
    window=tk.Tk()
    # messagebox.showinfo(date,'今日成交已经保存')
    tk.Label(window,text='{}\n今日债券成交已保存'.format(date)).pack()
    window.mainloop() # 会阻塞进程


class Timing:
    def __init__(self,title='同业成交爬虫'):
        self.no_need_window = False
        self.title=title

        self.th = threading.Thread(target=self.start_tk_info) # 弹窗的线程
        self.th.setDaemon(True)
        self.th.start()

        time.sleep(1)
        pass

    def start_tk_info(self):
        """
        用来提示定时到达，程序开始运行的弹窗
        :return: 无
        """
        print(threading.current_thread())
        now_time=datetime.datetime.now().time()
        self.window=tk.Tk()
        self.window.title('{} 已开始运行'.format(self.title))
        tk.Label(self.window,text='{} 已开始运行（本窗口可关闭）'.format(self.title)).grid(row=0,column=0,columnspan=2)
        self.text=tk.Text(self.window,height=2,width=20)
        self.text.grid(row=1,column=0)
        self.text.insert(tk.END,str(now_time))
        self.text_result=tk.Text(self.window,height=2,width=20)
        self.text_result.grid(row=1,column=1)
        self.text_result.insert(tk.END,'初始化')
        self.window.mainloop()
        self.window.quit()
        self.text=None
        self.window=None
        self.text_result=None
        gc.collect()
        print('上一进程关闭完成')

    def log_event(self,strr:str):
        """
        将结果输出到tkinter框中
        :return:
        """
        if self.th.is_alive() and hasattr(self, 'text_result'):  # 前面也是为了确保已经初始化完成
            self.text_result.delete(0.0, tk.END)  # 刷新时间
            self.text_result.insert(tk.END, strr)
        else:
            pass

    def sleep(self,wait_time:int):
        """
        休眠函数，每一秒刷新一次
        :param wait_time: 休眠时间（s)
        :return:
        """
        for i in range(wait_time, 0, -1):  # 延时
            now_time = str(datetime.datetime.now())[:19]
            print('\r{}s后再次获取  {}'.format(i, now_time), end='')
            if self.th.is_alive() and hasattr(self,'text'): # 前面也是为了确保已经初始化完成
                self.text.delete(0.0, tk.END)  # 刷新时间
                self.text.insert(tk.END, now_time)
            else:
                pass
            time.sleep(1)

    def th2(self):
        th2 = threading.Thread(target=self.start_tk_info)
        self.th=threading.Thread(target=self.start_tk_info)
        self.th.setDaemon(True)

        self.th.start()

    def main_loop(self,func,wait_time=5,rule='weekday==3 and hour>9 and hour <=18'):
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
            if eval(rule) :    # 规定的时间
                # self.window.destroy()
                print('开始运行')
                if self.no_need_window==False and not self.th.is_alive(): # 程序初始运行，打开窗口
                    time.sleep(1)
                    # 建立新线程打开窗口
                    print('开始打开窗口')

                    self.th = threading.Thread(target=self.start_tk_info)
                    self.th.setDaemon(True)
                    self.th.start()
                    time.sleep(1) # 第一次得等初始化完，不然直接开始text时，text还没初始化，此处不能使用self.sleep()
                else :
                    pass
                '''函数在这里！！！'''
                func()
                self.log_event('已运行完成')
                # 延时5s
                self.sleep(wait_time)
                self.no_need_window=True
            else: # 非所需时间
                self.no_need_window = False  # 重置，下次还是需要窗口
                print('  时间未到'.format(date_time),end='')
                self.log_event('时间未到')
                self.sleep(wait_time) # 延时1s

if __name__ == '__main__':
    print('成交数据每日爬虫')
    # 工作日获取债券信息
    Timing().main_loop(func=fetch_bond_info,wait_time=1,rule='weekday<5 and tim>"20:11:00"')
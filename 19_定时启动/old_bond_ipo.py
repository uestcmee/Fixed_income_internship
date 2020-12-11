# 星期三自动开始获取国债数据
# 开始获取后弹窗提示
# 这里还是不要传参的好，如果有取消延时的情况直接递归好了

import datetime
import time
import bond_remind_tkinter
import tkinter as tk
import threading

def tk_info():
    global window,text
    now_time=date_time.time()
    window=tk.Tk()
    window.title('国债发行检测已开始运行')
    tk.Label(window,text='国债发行检测已开始运行').grid(row=0,column=0)
    text=tk.Text(window,height=2,width=20)
    text.grid(row=1,column=0)
    text.insert(tk.END,str(now_time))
    window.mainloop()

#### 初始函数区
info_0 = bond_remind_tkinter.get_url()
for i in info_0:
    print(i[0])  # 初始标题
no_need_window=False # 默认打开提示窗口

while True: # 定时启动

    global date,window,text
    ### 更新时间区
    date_time = datetime.datetime.today()
    weekday = date_time.weekday()
    date, hour, mins = date_time.date(), date_time.hour, date_time.minute

    ### 时间判断区
    '''修改这里！！！'''
    if weekday==2 and hour>9 and hour <=18 :    # 星期三，早上九点开始运行，晚上7点之后结束
        if 't' not in locals(): # 程序初始运行，打开窗口
            t=threading.Thread(target=tk_info)
            t.start()
        elif not t.is_alive() and no_need_window==False:  # 窗口被关闭，但已经进入下一次提醒
            t=threading.Thread(target=tk_info)
            t.start()
        else :
            pass

        info_0=bond_remind_tkinter.main_fun(info_0) # 主函数，更新比较基准
        # 延时5s ,延时放外面只用写一个函数，但是要传参
        for i in range(5, 0, -1):# 延时
            now_time = str(datetime.datetime.now())[:19]
            print('\r{}s后再次获取  {}'.format(i,now_time), end='')
            if t.is_alive():
                text.delete(0.0,tk.END)
                text.insert(tk.END,now_time)
            else:
                no_need_window=True # 本日不再开窗口
            time.sleep(1)
    else:
        no_need_window = False  # 重置，下次还是需要窗口
        if 't' in locals() and t.is_alive(): # 关闭窗口
            window.destroy()
        print('\r时间未到，半小时后再试:{}'.format(date_time))
        time.sleep(1800) # 延时半小时
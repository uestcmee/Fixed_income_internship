# 定期获取数据，定时模块单独封装
# 后期可以使用mainloop文件进行定时
import datetime
import time,os
import tkinter as tk
import threading
import gc

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


from timed_start import Timing

if __name__ == '__main__':
    print('成交数据每日爬虫')
    # 工作日获取债券信息
    Timing(title='债券成交爬虫',rule='weekday<5 and tim>"20:11:00"').main_loop(func=fetch_bond_info,wait_time=5)
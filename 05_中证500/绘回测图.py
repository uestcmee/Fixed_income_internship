# coding:utf-8
import pandas as pd
file='./data/CSI.csv'
import matplotlib.pyplot as plt
import time
import sys
from load_file import load_file
import numpy as np


class STG_Return():

    def __init__(self,file_name=None,l_range = range(12, 31, 2),s_range = range(2, 12)):
        # 需要输入文件名
        assert file_name!=None
        # 载入文件
        self.close_data = load_file(file_name).read_file()
        # year range从loadfile中传递？
        self.time_list=self.get_ftd_list()
        print(self.time_list)
        self.ret_list = {}
        # MACD指标选择的长短期为12,26
        self.year_range=range(2006,2021)
        self.l_range = l_range  # 长期均线选择
        self.s_range = s_range  # 短期均线选择
        self.fac_range = [i / 100 for i in range(96, 106, 2)]
        self.main_loop()


    def get_ftd_list(self):# 获取每年基准交易日的时间
        ftd_list=[]
        for year in self.year_range:
            for t in range(1,10):
                try:
                    day = '{}-01-0{}'.format(year, t) # wind日期格式
                    # day = '{}/1/{}'.format(year, t)# csmar 日期格式
                    buffer = self.close_data.loc[day]
                    ftd_list.append(day)
                    break
                except:
                    pass
        return ftd_list


    def main_loop(self):
        t0 = time.time()

        for l_fac in [1]:
            for s_fac in [1.06]:
                # 取不同的上下限
                for long in [14]:
                    for short in [3]:
                        if long <= short:  # 如果上下限不合理，跳过
                            self.ret_list[str(long) + '_' + str(short)] = [0 for i in range(len(self.time_list))]
                            continue
                        tot_time = time.time() - t0
                        print('\r{} min : {} sec   '.format(int(tot_time / 60), int(tot_time % 60)), end='')
                        # ======开始进入收益率计算======
                        y5_r = self.cal_ma(long, short, l_fac=l_fac, s_fac=s_fac)
                        self.ret_list[str(long) + '_' + str(short)] = y5_r
                        print('{}_{}:{}'.format(long, short, y5_r))
                        sys.exit(1)

                # 命名方法：长期的乘数+短期的乘数
                self.output(self.ret_list, out_file=str(l_fac) + '_' + str(s_fac) + '.csv')


    def cal_ma(self,long=20,short=5,l_fac=1.03,s_fac=1.03):
        # long为长的均线，short为短的均线
        # 初始化收盘价dataframe
        self.close_data['20avg']=self.close_data['close'].rolling(window=long).mean().shift()
        self.close_data['5avg']=self.close_data['close'].rolling(window=short).mean().shift()
        # print(self.close_data)

        # pandas 的索引实在是太慢了，直接用lastday记录上一天的
        last_day=[-1,1] # 是否持有,策略总回报
        start_day=0
        year5=[]
        # print(len(self.close_data.index))
        for index,day  in enumerate (self.close_data.index[start_day:]):
            index=index+start_day
            if index==start_day:
                continue
            [close_p,earning,avg20,avg5]=self.close_data.loc[day][:4]
            # 主要的判断是否持有的语句
            if close_p>avg20*l_fac and close_p<avg5*s_fac:
                hold_flag=1
                # print(day)
            else:
                hold_flag=0
            [hold_flag_,last_return]=last_day
            if  hold_flag_==1 :  # 上一日选择持有，则本日计算收益率
                tot_return = last_return*(earning/100+1) # 上日累计收益率乘本日收益率
            else:
                tot_return = last_return
            tot_return=round(tot_return,6)
            last_day=[hold_flag,tot_return]

            year5.append(tot_return)
        year5.insert(0,1)
        year5 = pd.DataFrame(np.array(year5)*1000)
        year5.index=self.close_data.index
        # print(year5)
        self.close_data.insert(0,'stg_r',year5)
        print(self.close_data)
        self.close_data[['close','stg_r']].plot()
        plt.show()
        sys.exit(1)
        return year5


    def output(self,ret_list,out_file='default.csv'):
        out_file='.\outfile\\'+out_file
        open(out_file,'w').close()
        f = open(out_file, 'a')

        line1_list = ['{}_y{}'.format(i, j) for i in self.s_range for j in self.year_range]  # 标题行
        f.write(','+','.join(line1_list) + '\n')
        for long in self.l_range:
            out_line=[str(long)]
            for short in self.s_range:
                out_line.append(str(ret_list[str(long) + '_' + str(short)])[1:-1])
            f.write(','.join(out_line)+'\n')
        f.close()

if __name__ == '__main__':
    STG_Return('./data/CSI.csv')
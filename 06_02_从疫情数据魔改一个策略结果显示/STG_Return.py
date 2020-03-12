# coding:utf-8
import pandas as pd
file='./data/CSI.csv'
from LoadFile import load_file
import numpy as np

class StgReturn:
    def __init__(self,file_name=None,l_fac=1.0,s_fac=1.0,year_range=range(2006,2021),lma = 20,sma =9):
        # 在此修改长短期均线长度
        # ========================
        self.lma = lma  # 长期均线选择
        self.sma = sma  # 短期均线选择
        self.year_range=year_range
        # ============================

        # 需要输入文件名
        assert file_name != None
        # 载入文件
        self.close_data = load_file(file_name).read_file()
        # year range从loadfile中传递？
        # print(self.time_list)
        self.ret_list = {}
        # MACD指标选择的长短期为12,26
        self.l_fac=l_fac
        self.s_fac=s_fac
        self.main_loop()


    def main_loop(self):
        # ======开始进入收益率计算======
        stg_r,idx_r = self.cal_ma(self.lma, self.sma, l_fac=self.l_fac, s_fac=self.s_fac)
        df=pd.DataFrame()
        df.insert(0,'stg',np.array(stg_r))
        df.insert(1,'idx',np.array(idx_r))

        # df.insert([1,1])
        df.index=self.close_data.index[1:]
        return df




    def cal_ma(self,long=20,short=5,l_fac=1.03,s_fac=1.03):
        # long为长的均线，short为短的均线
        # 初始化收盘价dataframe
        self.close_data['20avg']=self.close_data['close'].rolling(window=long).mean().shift()
        self.close_data['5avg']=self.close_data['close'].rolling(window=short).mean().shift()
        # print(self.close_data)

        # pandas 的索引实在是太慢了，直接用lastday记录上一天的
        last_day=[-1,1] # 是否持有,策略总回报
        start_day=0
        stg_r,idx_r=[],[]
        idr=1
        for index,day  in enumerate (self.close_data.index[start_day:]):
            index=index+start_day
            # 跳过首日
            if index==start_day:
                continue
            [close_p,earning,avg20,avg5]=self.close_data.loc[day][:4]

            # 主要的判断是否持有的语句
            if close_p>avg20*l_fac and close_p<avg5*s_fac:
                hold_flag=1
            else:
                hold_flag=0

            [hold_flag_,last_return]=last_day
            if  hold_flag_==1 :  # 上一日选择持有，则本日计算收益率
                tot_return = last_return*(earning/100+1) # 上日累计收益率乘本日收益率
            else:
                tot_return = last_return
            idr*=(earning/100+1)
            stg_r.append(round(tot_return,6))
            idx_r.append(round(idr,6))
            tot_return=round(tot_return,6)
            last_day=[hold_flag,tot_return]

        return stg_r,idx_r





if __name__ == '__main__':
    StgReturn('./data/CSI.csv')
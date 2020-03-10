# coding:utf-8
import pandas as pd
file='./data/CSI.csv'
import matplotlib.pyplot as plt
import time,sqlite3
import sys
from LoadFile import load_file


class StgReturn:
    def __init__(self,file_name=None,l_fac=1.0,s_fac=1.0,year_range=range(2006,2021),l_range = range(12, 31, 2),s_range = range(2, 12)):
        # 在此修改长短期均线长度
        # ========================
        self.l_range = l_range  # 长期均线选择
        self.s_range = s_range  # 短期均线选择
        self.year_range=year_range
        # ============================

        # 需要输入文件名
        assert file_name != None
        # 载入文件
        self.close_data = load_file(file_name).read_file()
        # year range从loadfile中传递？
        self.time_list=self.get_ftd_list()
        # print(self.time_list)
        self.ret_list = {}
        # MACD指标选择的长短期为12,26
        self.l_fac=l_fac
        self.s_fac=s_fac


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

        # ======开始进入收益率计算======
        # 取不同的上下限
        self.ret_list={}
        for long in self.l_range:
            for short in self.s_range:
                tot_time = time.time() - t0
                print('\r{} min : {} sec   '.format(int(tot_time / 60), int(tot_time % 60)), end='')
                y5_r = self.cal_ma(long, short, l_fac=self.l_fac, s_fac=self.s_fac)
                self.ret_list[str(long) + '_' + str(short)] = y5_r
                for index,year in enumerate(self.time_list):
                    year=int(year[:4])
                    self.ToSQL(['\'000905\'',self.l_fac,self.s_fac,long,short,self.year_range[0],year,y5_r[index]])
                print('{}_{}:{}'.format(long, short, y5_r))
        # 取消了csv形式的输出
        # self.output(out_file=str(self.l_fac) + '_' + str(self.s_fac) + '.csv')

        return self.ret_list

    def ToSQL(self,word):
        """CREATE TABLE returns
            (
            ID int  identity (1,1) ,
            StockID varchar(20),
            LongFac float,
            ShortFac float,
            LongMA int,
            ShortMA int,
            StartYear int,
            EndYear int,
            Return float,
            PRIMARY KEY(ID)
            );
        """
        # print(self.ret_list)
        conn = sqlite3.connect('CSI.db')
        cursor = conn.cursor()
        # print('INSERT INTO returns values (NULL,{})'.format(','.join([str(i) for i in word])))
        cursor.execute('REPLACE INTO returns values (NULL,{})'.format(','.join([str(i) for i in word])))

        cursor.close()
        conn.commit()
        conn.close()
        pass



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
            tot_return=round(tot_return,6)
            last_day=[hold_flag,tot_return]
            if str(day)[:10] in self.time_list:
                year5.append(tot_return)
        return year5


    def output(self,out_file='default.csv'):

        out_file='.\\'+out_file
        open(out_file,'w').close()
        f = open(out_file, 'a')
        # print(self.ret_list)
        # print(self.time_list)
        line1_list = ['{}_y{}'.format(i, j) for i in self.s_range for j in self.year_range]  # 标题行
        f.write(','+','.join(line1_list) + '\n')
        for long in self.l_range:
            out_line=[str(long)]
            for short in self.s_range:
                out_line.append(str(self.ret_list[str(long) + '_' + str(short)])[1:-1])
            f.write(','.join(out_line)+'\n')
        f.close()

if __name__ == '__main__':
    StgReturn('./data/CSI.csv',l_range = range(27, 31, 2),s_range = range(10, 12))
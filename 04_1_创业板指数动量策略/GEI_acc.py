# coding:utf-8
import pandas as pd
file='GE IDX.csv'
import matplotlib.pyplot as plt
import seaborn as sns
import time
tot_data=pd.read_csv(file,index_col=1,names=['','open_p','long','short','close','trade','trade_amount','earning'])
tot_data.index=pd.DatetimeIndex(tot_data.index)
price_data=tot_data[['close','earning']]

# 先不获取指数收益率了，等以后单独获取

# 我也不知道为什么要加这句话，但是不加会报错A value is trying to be set on a copy of a slice from a DataFrame
# 操作的表格转换为close_data
close_data=price_data.copy()
close_data.drop((x for x in price_data.index if price_data.loc[x][0]==0),inplace=True)

last_day=[-1,1] # 是否持有,策略总回报

def cal_ma(long=20,short=5,l_fac=1.03,s_fac=1.03):
    # long为长的均线，short为短的均线
    # 初始化收盘价dataframe
    close_data['20avg']=close_data['close'].rolling(window=long).mean().shift()
    close_data['5avg']=close_data['close'].rolling(window=short).mean().shift()

    # pandas 的索引实在是太慢了，直接用lastday记录上一天的
    global last_day
    start_day=0
    time_list=['2016-02-15','2017-02-14','2018-02-14','2019-02-14','2020-02-14']
    year5=[]
    for index,day  in enumerate (close_data.index[start_day:]):
        index=index+start_day
        if index==start_day:
            continue
        [close_p,earning,avg20,avg5]=close_data.loc[day][:4]
        # 主要的判断是否持有的语句
        if close_p>avg20*l_fac and close_p<avg5*s_fac:
            hold_flag=1
        else:
            hold_flag=0
        [hold_flag_,last_return]=last_day
        if  hold_flag_==1:  # 上一日选择持有，则本日计算收益率
            tot_return = last_return*(earning/100+1) # 上日累计收益率乘本日收益率
        else:
            tot_return = last_return
        tot_return=round(tot_return,6)
        last_day=[hold_flag,tot_return]
        if str(day)[:10] in time_list:
            year5.append(tot_return)
    return year5


def output(ret_list,out_file='default.csv'):
    global l_range,l_range
    out_file='.\outfile\\'+out_file
    open(out_file,'w').close()
    f = open(out_file, 'a')

    line1_list = ['{}_y{}'.format(i, j) for i in s_range for j in range(16, 21)]  # 标题行
    f.write(','+','.join(line1_list) + '\n')
    for long in l_range:
        out_line=[str(long)]
        for short in s_range:
            out_line.append(str(ret_list[str(long) + '_' + str(short)])[1:-1])
        f.write(','.join(out_line)+'\n')
    f.close()


ret_list={}
# MACD指标选择的长短期为12,26
t0=time.time()

# 长期均线选择
l_range=range(12,31,2)
# 短期均线选择
s_range=range(2,12)

fac_range=[i/100 for i in range(96,106,2)]

for l_fac in fac_range:
    for s_fac in fac_range:
        # 取不同的上下限
        for long in l_range:
            for short in s_range:
                last_day = [-1, 1]  # 是否持有,策略总回报
                if long<=short:# 如果上下限不合理，跳过
                    ret_list[str(long) + '_' + str(short)] = [0 for i in range(5)]
                    continue
                tot_time = time.time() - t0
                print('\r{} min : {} sec   '.format(int(tot_time / 60), int(tot_time % 60)), end='')
                y5_r=cal_ma(long,short,l_fac=l_fac,s_fac=s_fac)
                ret_list[str(long)+'_'+str(short)]=y5_r
                print('{}_{}:{}'.format(long,short,y5_r))

        # 命名方法：长期的乘数+短期的乘数
        output(ret_list,out_file=str(l_fac)+'_'+str(s_fac)+'.csv')



def plott():
    sns.set()

    # 肯定有更好的方法，可是我不知道
    scatter=pd.DataFrame([[date,close_data['tot_return'].loc[date]] for date in close_data.index if close_data['hold_flag'].loc[date]==1])
    scatter.set_axis(['date','return'],1,inplace=True)

    scatter=scatter.set_index('date')

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(close_data[['idx_return','tot_return']])
    ax.bar(scatter.index,height=scatter['return'],width=1,linewidth=0,color='grey',alpha=0.3)
    plt.show()
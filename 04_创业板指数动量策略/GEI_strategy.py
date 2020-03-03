# coding:utf-8
import pandas as pd
file='GE IDX.csv'
import matplotlib.pyplot as plt
import seaborn as sns
import time
tot_data=pd.read_csv(file,index_col=1,names=['','open_p','high','low','close','trade','trade_amount','earning'])
tot_data.index=pd.DatetimeIndex(tot_data.index)

price_data=tot_data[['close','earning']]

# 我也不知道为什么要加这句话，但是不加会报错A value is trying to be set on a copy of a slice from a DataFrame
# 操作的表格转换为close_data
close_data=price_data.copy()
close_data.drop((x for x in price_data.index if price_data.loc[x][0]==0),inplace=True)

def cal_ma(long=20,short=5):
    # long为长的均线，short为短的均线
    close_data['20avg']=close_data['close'].rolling(window=long).mean()
    close_data['5avg']=close_data['close'].rolling(window=short).mean()
    close_data['tot_return']=1 # 策略总回报
    close_data['hold_flag']=-1 # 是否持有
    close_data['idx_return']=1 # 指数总回报
    #print(close_data.describe())

    for index,day  in enumerate (close_data.index[455:]):
        index=index+455
        if index==455:
            continue
        [close_p,earning,avg20,avg5]=close_data.loc[day][:4]
        if close_p>avg20*1.03 and close_p<avg5*1.03:
            hold_flag=1
        else:
            hold_flag=0
        hold_flag_=close_data['hold_flag'].iloc[index-1] # 上一日是否持有
        last_return=close_data['tot_return'].iloc[index-1]# 上一日的持有收益率
        tot_return=last_return
        if  hold_flag_==1:  # sold
            tot_return = last_return*(earning/100+1) # 上日累计收益率乘本日收益率
        idx_return=close_data['idx_return'].iloc[index-1]*(earning/100+1)
        close_data.loc[day]=[close_p,earning,avg20,avg5]+[tot_return,hold_flag,idx_return]

    #print(close_data[['idx_return','tot_return','hold_flag']])
    year5=close_data.loc['2020-02-14'][['tot_return','idx_return']]
    print(year5)

    return year5

ret_list={}
# 12,26
t0=time.time()
for high in range(18,30):
    for low in range(5,18):
        tot_time = time.time() - t0
        print('\r{} min : {} sec   '.format(int(tot_time / 60), int(tot_time % 60)), end='')
        five_year=cal_ma(high,low);
        ret_list[str(high)+'_'+str(low)]=five_year
        print('{}_{}:{}'.format(high,low,five_year))
#print(ret_list)
for high in range(18,30):
    for low in range(5,18):
        print(ret_list[str(high)+'_'+str(low)],end=',')
    print('')


def plott():
    sns.set_style('whitegrid')

    # 肯定有更好的方法，可是我不知道
    scatter=pd.DataFrame([[date,close_data['tot_return'].loc[date]] for date in close_data.index if close_data['hold_flag'].loc[date]==1])
    scatter.set_axis(['date','return'],1,inplace=True)

    scatter=scatter.set_index('date')

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(close_data[['idx_return','tot_return']])
    ax.bar(scatter.index,height=scatter['return'],width=1,linewidth=0,color='grey',alpha=0.3)
    plt.show()
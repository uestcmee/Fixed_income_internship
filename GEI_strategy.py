# coding:utf-8

import pandas as pd
file='GE IDX.csv'
import matplotlib.pyplot as plt
import seaborn as sns
tot_data=pd.read_csv(file,index_col=1,names=['','open_p','high','low','close','trade','trade_amount','earning'])
tot_data.index=pd.DatetimeIndex(tot_data.index)

price_data=tot_data[['close','earning']]


# for x in price_data.index:
#     print(price_data.loc[x][0])
#     if price_data.loc[x][0]==0.0:
#         price_data.drop(x,inplace=True)

# 我也不知道为什么要加这句话，但是不加会报错A value is trying to be set on a copy of a slice from a DataFrame
close_data=price_data.copy()
close_data.drop((x for x in price_data.index if price_data.loc[x][0]==0),inplace=True)

close_data['20avg']=close_data['close'].rolling(window=20).mean()
close_data['5avg']=close_data['close'].rolling(window=5).mean()

#print(close_data.head(30))

# sns.set_style('whitegrid')
# close_data[['close','20avg','5avg']].plot()
# plt.show()



close_data['tot_return']=1
close_data['hold_flag']=-1
close_data['idx_return']=1
#print(close_data.describe())

for index,day  in enumerate (close_data.index):
    if index==0:
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

# print(close_data[['idx_return','tot_return','hold_flag']])

sns.set_style('whitegrid')

# 肯定有更好的方法，可是我不知道
scatter=pd.DataFrame([[date,close_data['tot_return'].loc[date]] for date in close_data.index if close_data['hold_flag'].loc[date]==1])
scatter.set_axis(['date','return'],1,inplace=True)

scatter=scatter.set_index('date')

# plt.subplots(2,1)
# plt.subplot(211)
# plt.plot(close_data[['tot_return','idx_return']])
# plt.subplot(212)
# plt.bar(scatter.index,height=scatter['return'],width=1)
# plt.show()
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(close_data[['idx_return','tot_return']])
ax.bar(scatter.index,height=scatter['return'],width=1,linewidth=0,color='grey',alpha=0.3)
plt.show()
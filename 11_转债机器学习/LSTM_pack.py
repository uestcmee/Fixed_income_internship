#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import math,os



# # 封装一个LSTM模型，方便使用
# * 输入收盘价数据，先使用一维数据
# * 按照lookback=20，预测后一天的涨跌情况
# * 70%的训练集，30%的测试集
# 

# In[22]:


def create_dataset(dataset, look_back=1):  # 后一个数据和前look_back个数据有关系
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back)]
        dataX.append(a)  # .apeend方法追加元素
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)  # 生成输入数据和输出数据


def train_model(train_x,train_y,look_back):
    
    model = Sequential()
    # input_shape为训练的输入形状，第一个数字为每次有多少个数据输入
    model.add(LSTM(11, input_shape=(1, look_back)))  # 隐层11个神经元 （可以断调整此参数提高预测精度）
    model.add(Dense(1)) # 输出层的个数（向后预测多少天？）
    model.compile(loss='mse', optimizer='adam')  # 评价函数mse，优化器adam
    model.fit(train_x, train_y, epochs=200, batch_size=100, verbose=0)  # 100次迭代
    model.save('./{}.h5'.format('myLSTM'))
    return model


def cal_the_return(testPredict,testY):
    # 测试集的实际收益率和测试集的预测收益率
    compare=pd.DataFrame({'pred_y':testPredict.T[0],'real_y':testY.T[0]})
    # 计算转债累计收益率
    accy=(compare['real_y']/100+1).cumprod()
    # 计算策略累计收益率
    accp=(pd.Series(compare['real_y'][compare['pred_y']>0],index=compare.index).fillna(0)/100+1).cumprod()

    compare['acc_y'] = accy # 累计收益率真实值
    compare['acc_p'] = accp # 预测累计收益率
    return compare

def data_processing(price_series,look_back):
    # 转换为收益率序列
    pct_chg_series=(price_series/price_series.shift(1)-1)[1:]

    # 进行归一化
    scaler = MinMaxScaler(feature_range=(0, 1))  # 定义归一化函数，归一化0-1
    scaler_series=scaler.fit_transform(np.array(pct_chg_series*100).reshape(len(pct_chg_series),1))
    train,test=scaler_series[0:int(len(scaler_series)*0.7)],scaler_series[int(len(scaler_series)*0.7):] # 对其进行训练和测试的划分
    
    # 对于训练集和测试集按照所需格式进行划分
    train_x,train_y=create_dataset(train,look_back=20) # 训练集
    test_x,test_y=create_dataset(test,look_back=20) # 测试集

    # 进行reshape，用于LSTM模型
    train_x=np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x=np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))
    return train_x,train_y,test_x,test_y,scaler
    
    
def LSTM_model(price_series):
    assert type(price_series)==type(pd.Series(dtype='float')),'请传入价格的pandas Series序列'
    
    look_back=20

    train_x,train_y,test_x,test_y,scaler=data_processing(price_series,look_back)
    
    print('开始训练')
    model=train_model(train_x,train_y,look_back)
    
    # 评估结果
    print('开始评估结果')
    train_predict=model.predict(train_x)
    test_predict=model.predict(test_x)
    # 反归一化
    train_predict=scaler.inverse_transform(train_predict)
    test_predict=scaler.inverse_transform(test_predict)
    test_y=scaler.inverse_transform(test_y)
    # 进行策略对比
    compare=cal_the_return(test_predict,test_y)
    # print(compare)
    return compare


# In[23]:


df=pd.read_excel('转债时间序列.xlsx',index_col=0)[:-7]
compare=LSTM_model(df['110031.SH'])


# In[24]:


compare


# In[25]:


compare.iloc[:,2:].plot()


# In[21]:


df['110031.SH'].plot()


# In[ ]:





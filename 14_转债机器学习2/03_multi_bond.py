#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn import metrics

import pandas as pd
import numpy as np


from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import math,os


# In[50]:


df_info=pd.read_excel('02_可转债基本面.xlsx',index_col=0)[:-7]
df_info.columns=list(map(lambda x:str(x)[:5].strip(),df_info.columns.tolist()))
df_info=df_info[(df_info['月成交金额']>100)&(df_info['发行信用等']!='A')&(df_info['发行信用等']!='A+')]
df_info=df_info[(df_info['上市公告日']<'2020-01-01')]


# In[51]:


df_price=pd.read_excel('01_转债价格序列.xlsx',index_col=0)[2:-7]
df_price=df_price.loc[:,df_info.index.tolist()]
df_price


# In[49]:


from 02_


# In[ ]:





# In[ ]:


def create_dataset(dataset, look_back=1):  # 后一个数据和前look_back个数据有关系
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back)]
        dataX.append(a)  # .apeend方法追加元素
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)  # 生成输入数据和输出数据


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


def data_processing_xgb(price_series,look_back):
    # 转换为收益率序列
    pct_chg_series=(price_series/price_series.shift(1)-1)[1:]

    # 进行归一化
    scaler = MinMaxScaler(feature_range=(0, 1))  # 定义归一化函数，归一化0-1
    scaler_series=scaler.fit_transform(np.array(pct_chg_series*100).reshape(len(pct_chg_series),1))
    train,test=scaler_series[0:int(len(scaler_series)*0.7)],scaler_series[int(len(scaler_series)*0.7):] # 对其进行训练和测试的划分
    
    # 对于训练集和测试集按照所需格式进行划分
    train_x,train_y=create_dataset(train,look_back=20) # 训练集
    test_x,test_y=create_dataset(test,look_back=20) # 测试集

    # 进行reshape，用于XGBoosting模型
    train_x=np.reshape(train_x, (train_x.shape[0], train_x.shape[1]))
    test_x=np.reshape(test_x, (test_x.shape[0], test_x.shape[1]))
    return train_x,train_y,test_x,test_y,scaler
    
    
def xgb_model(price_series):
    assert type(price_series)==type(pd.Series(dtype='float')),'请传入价格的pandas Series序列'
    
    look_back=20
    train_x,train_y,test_x,test_y,scaler=data_processing_xgb(price_series,look_back)
    dtrain = xgb.DMatrix(train_x, label = train_y)
    dtest = xgb.DMatrix(test_x)
    # 参数设置
    params={'booster':'gbtree',
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth':4,
        'lambda':10,
        'subsample':0.75,
        'colsample_bytree':0.75,
        'min_child_weight':2,
        'eta': 0.025,
        'seed':0,
        'nthread':8,
         'silent':1}

    watchlist = [(dtrain,'train')]
    # 进行训练
    bst=xgb.train(params,dtrain,num_boost_round=1000,evals=watchlist,verbose_eval=100)
    # 预测
    test_predict=bst.predict(dtest)
    # 反归一化
    test_predict=scaler.inverse_transform(test_predict.reshape(len(test_predict),1))# 需要reshape一下，以便inverse_transform
    test_y=scaler.inverse_transform(test_y)
    # 进行策略对比
    compare=cal_the_return(test_predict,test_y)
    # print(compare)
    return compare,bst


# In[ ]:





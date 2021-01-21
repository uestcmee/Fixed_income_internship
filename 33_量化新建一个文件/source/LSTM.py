# -*- coding: utf-8 -*-
"""
 LSTM prediction
"""
# 导入库函数

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM



def lstm_model(trainX_LSTM,trainY):
    model = Sequential()

    model.add(LSTM(11, input_shape=(24, 10)))  # 隐层11个神经元 ,输入数据格式为24维*10天
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')  # 评价函数mse，优化器adam
    model.fit(trainX_LSTM, trainY, epochs=50, batch_size=100, verbose=1)  # 100次迭代
    return model

if __name__ == '__main__':
    pass
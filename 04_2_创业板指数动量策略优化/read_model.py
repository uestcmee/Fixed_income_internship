# -*- coding: utf-8 -*-
"""
 LSTM prediction
@author: ljq
"""
# 导入库函数
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
import math
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# 读取数据
data = read_csv('r.csv')  # csv文件 n*1 ,n代表样本数，反应时间序列，1维数据

values1 = data.values;
dataset = values1[:, 0].reshape(-1, 1)  # 注意将一维数组，转化为2维数组
dataset = dataset.astype('float32')  # 将数据转化为32位浮点型，防止0数据


def cal_the_return(testPredict,testY):
    compare=pd.DataFrame(testPredict,)
    compare['testy']=testY[0]
    compare.columns=['predy','testy']
    compare.to_csv('compare.csv')
    accy = [1]
    accp = [[1]for i in range(6)]
    for row in compare.index:
        if row == 0:
            continue
        pred = compare['predy'].loc[row]
        real = compare['testy'].loc[row]
        accy.append(accy[row - 1] * (1 + real))
        for i in range(6):
            if pred > i*0.001:  # 如果预期收益率大于0.1%*i，则当日持有
                accp[i].append(accp[i][row - 1] * (1 + real))
            else:
                accp[i].append(accp[i][row - 1])
    compare['acc_y'] = accy
    for i in range(6):
        compare['acc_p'+str(i)] = accp[i]

    return compare

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):  # 后一个数据和前look_back个数据有关系
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)  # .apeend方法追加元素
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)  # 生成输入数据和输出数据


numpy.random.seed(7)  # 随机数生成时算法所用开始的整数值

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))  # 归一化0-1
dataset = scaler.fit_transform(dataset)
# split into train and test sets  #训练集和测试集分割
train_size = int(len(dataset) * 0.67)  # %67的训练集，剩下测试集
test_size = len(dataset) - train_size
train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]  # 训练集和测试集

# use this function to prepare the train and test datasets for modeling
look_back = 20
trainX, trainY = create_dataset(train, look_back)  # 训练输入输出
testX, testY = create_dataset(test, look_back)  # 测试输入输出

# reshape input to be [samples, time steps, features]#注意转化数据维数
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


# load model
model=load_model('my_model.h5')
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)


# 数据反归一化
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])



trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
print('Train Score: %.5f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
print('Test Score: %.5f RMSE' % (testScore))


trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict


# plot baseline and predictions
plt.figure(figsize=(20, 6))
l1, = plt.plot(scaler.inverse_transform(dataset), color='red', linewidth=5, linestyle='--')
l2, = plt.plot(trainPredictPlot, color='k', linewidth=4.5)
l3, = plt.plot(testPredictPlot, color='g', linewidth=4.5)
plt.ylabel('Height m')
plt.legend([l1, l2, l3], ('raw-data', 'true-values', 'pre-values'), loc='best')
plt.title('LSTM Gait Prediction')
plt.savefig('LSTM Gait Prediction.svg',format='svg')
plt.show()

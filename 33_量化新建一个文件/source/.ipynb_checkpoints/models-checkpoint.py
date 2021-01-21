from keras.models import Sequential  # 采用贯序模型
from keras.layers import Input, Dense, Dropout, Activation
import pandas as pd
from keras.optimizers import SGD
import numpy as np
import xgboost as xgb
from keras.layers import LSTM


def correlation(dataset, threshold:float=0.8):
    """
    数据降维，去掉相关系数大于threhold的列
    :param dataset: 传入pandas.DataFrame
    :param threshold:
    :return: 处理后的DataFrame
    """
    assert isinstance(dataset,pd.core.frame.DataFrame),'请传入pandas.DataFrame'
    col_corr = set() # Set of all the names of deleted columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i, j] >= threshold) and (corr_matrix.columns[j] not in col_corr):
                colname = corr_matrix.columns[i] # getting the name of column
                col_corr.add(colname)
                if colname in dataset.columns:
                    del dataset[colname] # deleting the column from the dataset
    return dataset


def ann_model(trainX,trainY,verbose=0):
    tBatchSize = 128
    '''第一步：选择模型'''
    model = Sequential()  # 采用贯序模型
    '''第二步：构建网络层'''
    '''构建网络只是构建了一个网络结构，并定义网络的参数，此时还没有输入的数据集'''
    # 构建的第一个层作为输入层
    # Dense 这是第一个隐藏层，并附带定义了输入层，该隐含层有500个神经元。输入则是 784个节点
    model.add(Dense(50, input_shape=(trainX.shape[1],)))  # 输入层，输入层将二维矩阵换成了一维向量输入
    model.add(Activation('relu'))  # 激活函数是relu
    model.add(Dropout(0.5))  # 采用50%的dropout  随机取一半进行训练

    # 构建的第2个层作为隐藏层2， （如果加上输入层，实际上是第三层）
    model.add(Dense(50))  # 隐藏层节点50个
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(50))  # 隐藏层3，节点50个
    model.add(Activation('relu'))
    # model.add(Dropout(0.5))

    # 构建的第3个层作为输出层
    model.add(Dense(1))  #

    '''第三步：网络优化和编译'''
    #   lr：大于0的浮点数，学习率
    #   momentum：大于0的浮点数，动量参数
    #   decay：大于0的浮点数，每次更新后的学习率衰减值
    #   nesterov：布尔值，确定是否使用Nesterov动量
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  # 优化函数，设定学习率（lr）等参数
    model.compile(loss='mean_squared_error', optimizer=sgd)  #均方误差作为损失函数，优化器为sgd

    # 开始训练
    model.fit(trainX, trainY, batch_size=tBatchSize, epochs=50, shuffle=True, verbose=verbose, validation_split=0.3)
    return model

def lstm_model(trainX_LSTM,trainY,verbose=0):
    model = Sequential()

    model.add(LSTM(11, input_shape=(24, 10)))  # 隐层11个神经元 ,输入数据格式为24维*10天
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')  # 评价函数mse，优化器adam
    model.fit(trainX_LSTM, trainY, epochs=50, batch_size=100, verbose=verbose)  # 100次迭代
    return model


def xbg_model(trainX,trainY):
    trainX=np.reshape(trainX,(trainX.shape[0],-1))
    # testX=np.reshape(testX,(testX.shape[0],-1))
    dtrain = xgb.DMatrix(trainX, label = trainY)
    # dtest = xgb.DMatrix(testX)
    # 参数设置
    params={
        'booster':'gbtree',
        'objective':'reg:squarederror',
        'eval_metric': 'auc',
        'max_depth':4,
        'lambda':10,
        'subsample':0.75,
        'colsample_bytree':0.75,
        'min_child_weight':2,
        'eta': 0.025,
        'seed':int(np.random.rand()*10000),#随机数的种子
        # 'nthread':8, #XGBoost运行时的线程数。缺省值是当前系统可以获得的最大线程数
        }

    watchlist = [(dtrain,'train')]
    # 进行训练
    model=xgb.train(params,dtrain,num_boost_round=1000,
                    evals=watchlist,verbose_eval=False) #,verbose_eval=1000
    return model

if __name__ == '__main__':
    pass
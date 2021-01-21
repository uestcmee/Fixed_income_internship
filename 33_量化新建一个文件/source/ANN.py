# 这是一个简单的全连接神经网络的例子。
from keras.models import Sequential  # 采用贯序模型
from keras.layers import Input, Dense, Dropout, Activation
from keras.optimizers import SGD


def ann_model(trainX,trainY):
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
    model.fit(trainX, trainY, batch_size=tBatchSize, epochs=50, shuffle=True, verbose=1, validation_split=0.3)
    return model

if __name__ == '__main__':
    pass
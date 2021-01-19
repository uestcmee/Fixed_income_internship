# =================== Test 1    Hello Keras for mnist==============================================================================
# 这是一个简单的全连接神经网络的例子。
from keras.models import Sequential  # 采用贯序模型
from keras.layers import Input, Dense, Dropout, Activation
from keras.models import Model
from keras.optimizers import SGD
from keras.datasets import mnist
import numpy as np
# import tensorboard

tBatchSize = 128
'''第一步：选择模型'''
model = Sequential()  # 采用贯序模型

'''第二步：构建网络层'''
'''构建网络只是构建了一个网络结构，并定义网络的参数，此时还没有输入的数据集'''
# 构建的第一个层作为输入层
# Dense 这是第一个隐藏层，并附带定义了输入层，该隐含层有500个神经元。输入则是 784个节点
model.add(Dense(500, input_shape=(784,)))  # 输入层，28*28=784 输入层将二维矩阵换成了一维向量输入
model.add(Activation('tanh'))  # 激活函数是tanh 为双曲正切  tanh(x) = sinh(x)/cosh(x) = (e^x - e^(-x))/(e^x + e^(-x))
model.add(Dropout(0.5))  # 采用50%的dropout  随机取一半进行训练

# 构建的第2个层作为隐藏层2， （如果加上输入层，实际上是第三层）
model.add(Dense(500))  # 隐藏层节点500个
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(500))  # 隐藏层3，节点500个
model.add(Activation('tanh'))
# model.add(Dropout(0.5))

# 构建的第3个层作为输出层
model.add(Dense(10))  # 输出结果是10个类别，所以维度是10
# softmax介绍可以参考https://blog.csdn.net/haolexiao/article/details/72757796
model.add(Activation('softmax'))  # 最后一层用softmax作为激活函数

'''第三步：网络优化和编译'''
#   lr：大于0的浮点数，学习率
#   momentum：大于0的浮点数，动量参数
#   decay：大于0的浮点数，每次更新后的学习率衰减值
#   nesterov：布尔值，确定是否使用Nesterov动量
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  # 优化函数，设定学习率（lr）等参数

# 只有通过了编译，model才真正的建立起来，这时候才能够被使用
# model.compile(loss='categorical_crossentropy', optimizer=sgd, class_mode='categorical') # 使用交叉熵作为loss函数 这是原例子，但是执行出错
model.compile(loss='categorical_crossentropy', optimizer=sgd)  # 使用交叉熵作为loss函数    # 去掉 class_mode 即可。可能是版本不同导致的？？？

'''
   第四步：训练
'''

# 数据集获取 mnist 数据集的介绍可以参考 https://blog.csdn.net/simple_the_best/article/details/75267863
(X_train, y_train), (X_test, y_test) = mnist.load_data()  # 使用Keras自带的mnist工具读取数据（第一次需要联网）

# 由于mist的输入数据维度是(num, 28, 28)，这里需要把后面的维度直接拼起来变成784维
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1] * X_train.shape[2])
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1] * X_test.shape[2])

# 这个能生成一个OneHot的10维向量，作为Y_train的一行，这样Y_train就有60000行OneHot作为输出
Y_train = (np.arange(10) == y_train[:, None]).astype(int)  # 整理输出
Y_test = (np.arange(10) == y_test[:, None]).astype(int)  # np.arange(5) = array([0,1,2,3,4])

'''
   .fit的一些参数
   batch_size：对总的样本数进行分组，每组包含的样本数量
   epochs ：训练次数
   shuffle：是否把数据随机打乱之后再进行训练
   validation_split：拿出百分之多少用来做交叉验证
   verbose：屏显模式 0：不输出  1：输出进度  2：输出每次的训练结果
'''
model.fit(X_train, Y_train, batch_size=tBatchSize, epochs=50, shuffle=True, verbose=2, validation_split=0.3)
# model.evaluate(X_test, Y_test, batch_size=200, verbose=0)


'''第五步：输出'''
print("test set")
# 误差评价 ：按batch计算在batch用到的输入数据上模型的误差
scores = model.evaluate(X_test, Y_test, batch_size=tBatchSize, verbose=0)
print("")
print("The test loss is %f" % scores)

# 根据模型获取预测结果  为了节约计算内存，也是分组（batch）load到内存中的，
result = model.predict(X_test, batch_size=tBatchSize, verbose=1)

# 找到每行最大的序号
result_max = np.argmax(result, axis=1)  # axis=1表示按行 取最大值   如果axis=0表示按列 取最大值 axis=None表示全部
test_max = np.argmax(Y_test, axis=1)  # 这是结果的真实序号

result_bool = np.equal(result_max, test_max)  # 预测结果和真实结果一致的为真（按元素比较）
true_num = np.sum(result_bool)  # 正确结果的数量
print("The accuracy of the model is %f" % (true_num / len(result_bool)))  # 验证结果的准确率

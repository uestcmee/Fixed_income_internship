# 国债期货量化策略


> `app.py`/`source`/`static`/`teamplates`文件是打算web端展示写的，可以先不管

目前采用了几种不同的机器学习模型对国债期货的30min数据进行学习和预测

## 数据文件

* [`T_30min.xls`](T_30min.xls)为简单的开高低收数据，
* [`T_30min with indicators.csv`](T_30min with indicators.csv)是曙子哥提取的部分特征数据


## 模型训练文件

* [`模型训练.ipynb`](1_1_模型训练.ipynb)最初的文件，简单实现了普通神经网络、LSTM、xgboost模型的预测
* [`模型训练_softmax.ipynb`](1_2_模型训练_softmax.ipynb)使用分类数据，将输入及预测分为涨跌两类
* [`更换数据文件.ipynb`](2_1_更换数据文件.ipynb)使用曙子哥的数据
* [`更换数据文件_softmax.ipynb`](2_2_更换数据文件_softmax.ipynb)使用曙子哥的数据
* [`模型打包.ipynb`](3_1_模型打包.ipynb)由于模型的收敛结果存在不确定性，多次训练观察结果稳定性


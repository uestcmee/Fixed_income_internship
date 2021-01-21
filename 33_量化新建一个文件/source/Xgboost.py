
import xgboost as xgb
import numpy as np


def xbg_model(trainX,trainY,lookback):
    trainX=np.reshape(trainX,(trainX.shape[0],-1))
    # testX=np.reshape(testX,(testX.shape[0],-1))

    #     train_x,train_y,test_x,test_y,scaler=data_processing_xgb(price_series,look_back)
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
    #     'seed':0,#随机数的种子
        # 'nthread':8, #XGBoost运行时的线程数。缺省值是当前系统可以获得的最大线程数
        }

    watchlist = [(dtrain,'train')]
    # 进行训练
    model=xgb.train(params,dtrain,num_boost_round=1000,evals=watchlist,verbose_eval=1000)
    return model

if __name__ == '__main__':
    pass
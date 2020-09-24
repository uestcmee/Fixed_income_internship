from sklearn import datasets
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn import metrics

# 导入鸢尾花的数据
iris = datasets.load_iris()
# 特征数据
data = iris.data[:100] # 有4个特征
# 标签
label = iris.target[:100]

# 提取训练集和测试集
# random_state：是随机数的种子。
train_x, test_x, train_y, test_y = train_test_split(data, label, random_state=0)

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

bst=xgb.train(params,dtrain,num_boost_round=100,evals=watchlist)
ypred=bst.predict(dtest)

# 设置阈值, 输出一些评价指标
# 0.5为阈值，ypred >= 0.5输出0或1
y_pred = (ypred >= 0.5)*1

# ROC曲线下与坐标轴围成的面积
print ('AUC: %.4f' % metrics.roc_auc_score(test_y,ypred))
# 准确率
print ('ACC: %.4f' % metrics.accuracy_score(test_y,y_pred))
print ('Recall: %.4f' % metrics.recall_score(test_y,y_pred))
# 精确率和召回率的调和平均数
print ('F1-score: %.4f' %metrics.f1_score(test_y,y_pred))
print ('Precesion: %.4f' %metrics.precision_score(test_y,y_pred))
metrics.confusion_matrix(test_y,y_pred)
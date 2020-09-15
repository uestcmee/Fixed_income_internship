import pandas as pd
import warnings
from sklearn.preprocessing import scale
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier

# import lightgbm as lgb


# 读取数据集
data_all = pd.read_csv('/home/infisa/wjht/project/DataWhale/data_all.csv', encoding='gbk')

# 划分为5折交叉验证数据集
df_y=data_all['status']
df_X=data_all.drop(columns=['status'])
df_X=scale(df_X,axis=0)  #将数据转化为标准数据
#构建模型

lr = LogisticRegression(random_state=2018,tol=1e-6)  # 逻辑回归模型

tree = DecisionTreeClassifier(random_state=2018) #决策树模型

svm = SVC(probability=True,random_state=2018,tol=1e-6)  # SVM模型

forest=RandomForestClassifier(n_estimators=100,random_state=2018) #　随机森林

Gbdt=GradientBoostingClassifier(random_state=2018) #CBDT

Xgbc=XGBClassifier(random_state=2018)  #Xgbc

gbm=lgb.LGBMClassifier(random_state=2018)  #lgb



def muti_score(model):
    warnings.filterwarnings('ignore')
    accuracy = cross_val_score(model, df_X, df_y, scoring='accuracy', cv=5)
    precision = cross_val_score(model, df_X, df_y, scoring='precision', cv=5)
    recall = cross_val_score(model, df_X, df_y, scoring='recall', cv=5)
    f1_score = cross_val_score(model, df_X, df_y, scoring='f1', cv=5)
    auc = cross_val_score(model, df_X, df_y, scoring='roc_auc', cv=5)
    print("准确率:",accuracy.mean())
    print("精确率:",precision.mean())
    print("召回率:",recall.mean())
    print("F1_score:",f1_score.mean())
    print("AUC:",auc.mean())



model_name=["lr","tree","svm","forest","Gbdt","Xgbc","gbm"]
for name in model_name:
    model=eval(name)
    print(name)
    # muti_score(model)


'''
lr
准确率: 0.7890191148682617
精确率: 0.6542724662896913
召回率: 0.3377975457965613
F1_score: 0.44525012166067884
AUC: 0.7840451024530857
tree
准确率: 0.6962524533638791
精确率: 0.39920670173446693
召回率: 0.4157413593052284
F1_score: 0.40705496051057793
AUC: 0.6029856787858856
svm
准确率: 0.787758390223099
精确率: 0.7351623295760905
召回率: 0.24060335431243626
F1_score: 0.36179547264664874
AUC: 0.7640376541388867
forest
准确率: 0.7921756804332226
精确率: 0.7135700690071172
召回率: 0.2867128441334693
F1_score: 0.40835414886475174
AUC: 0.7752164698827589
Gbdt
准确率: 0.7938590063951863
精确率: 0.6604108594441386
召回率: 0.36633732991104395
F1_score: 0.4708811551285791
AUC: 0.7888240065764295
Xgbc
准确率: 0.7982740847293591
精确率: 0.6829783239831001
召回率: 0.3663162336064133
F1_score: 0.47673826685376613
AUC: 0.7914190511145234
gbm
准确率: 0.79049080811139
精确率: 0.6421783397519263
召回率: 0.3730354066312717
F1_score: 0.47150438344663004
AUC: 0.7776116341798183
'''

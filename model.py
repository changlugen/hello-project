from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import datetime
warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import confusion_matrix
import scorecardpy as sc
import joblib


#读取数据
path = '/Users/mac/Desktop/'
file_name = ['loanData.csv', 'loan_insight.csv']
loanData = pd.read_csv(path + file_name[0])
loan_insight = pd.read_csv(path + file_name[1])

loanData_new = loanData.iloc[:,[3, 5, 8, 10 ,12]]
loan_insight_new = loan_insight.iloc[:, 1:]

#拼接数据框
merge_data = pd.concat([loanData_new, loan_insight_new], axis=1)

#贷款时间升序排序
merge_data_sort = merge_data.sort_values('loan_time')

#去重
merge_data_duplicate = merge_data_sort.drop_duplicates(['user'])

#去除无用数据
data_filter = merge_data_duplicate[5:]

#预处理后的数据框
data_prepcs = data_filter[data_filter['apply_type'] =='首单']
data_prepcs = data_filter[data_filter['status'] !='否']
#data_prepcs.tail()



#删除无用变量
data_dateDiff = data_prepcs.drop(['user', 'channel', 'loan_time', 'apply_type'], axis=1)

#选取有效数据
data_dateDiff = data_dateDiff[230:]

#将无改成当天时间
data_dateDiff['最近一次贷款时间'].replace('无', datetime.datetime.today().strftime('%Y-%m-%d'), inplace=True)
data_dateDiff['最近一次贷款时间'] = pd.to_datetime(data_dateDiff['最近一次贷款时间'])

#求当天时间和最近一次贷款时间的差值
date_today = pd.to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))
data_dateDiff['最近一次贷款时间'] = data_dateDiff['最近一次贷款时间'].apply(lambda x: (date_today-x).days)

data_dateDiff['最近一次贷款时间'] = data_dateDiff['最近一次贷款时间'].astype('str')
data_dateDiff['最近一次贷款时间'] = data_dateDiff['最近一次贷款时间'].replace('0', '365')

#data_dateDiff.info()



#将无改成当天时间
data_dateDiff['最后一次逾期时间'].replace('无', datetime.datetime.today().strftime('%Y-%m-%d'), inplace=True)
data_dateDiff['最后一次逾期时间'] = pd.to_datetime(data_dateDiff['最后一次逾期时间'])

#求当天时间和最近一次贷款时间的差值
date_today = pd.to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))
data_dateDiff['最后一次逾期时间'] = data_dateDiff['最后一次逾期时间'].apply(lambda x: (date_today-x).days)

data_dateDiff['最后一次逾期时间'] = data_dateDiff['最后一次逾期时间'].astype('str')
data_dateDiff['最后一次逾期时间'] = data_dateDiff['最后一次逾期时间'].replace('0', '365')

#data_dateDiff.info()



data_dateDiff.iloc[:, 5:8] = data_dateDiff.iloc[:, 5:8].replace('无', 0).astype('int')
data_dateDiff['最大逾期金额范围'] = data_dateDiff['最大逾期金额范围'].replace('无', 0)
data_dateDiff['最长逾期天数'] = data_dateDiff['最长逾期天数'].replace('无', 0)
data_dateDiff['当前逾期机构数'] = data_dateDiff['当前逾期机构数'].replace('无', 0).astype('int')



#响应变量
data_Y = data_dateDiff.iloc[:,0]

#解释变量
data_X = data_dateDiff.iloc[:, 1:]

data = pd.concat([data_X, data_Y], axis=1)
data = data.drop('最近一次贷款时间', axis=1)

#响应变量01编码
labelEncoder = LabelEncoder()
data['status'] = labelEncoder.fit_transform(data['status'].values)
data = data.astype('str')



#默认删除信息只<0.02，缺失率>95%，单类别比例>95%的变量
dt_s = sc.var_filter(data, y='status')
print('变量预处理前后变化：', data.shape, '->', dt_s.shape)
#print(data.columns)
#print(dt_s.columns)



#分箱WOE转换
bins = sc.woebin(dt_s, y='status')
# bins

train, test = sc.split_df(dt_s, 'status').values()
print('训练集、测试集划分比例为：', train.shape[0], ':', test.shape[0])

train_woe = sc.woebin_ply(train, bins)
test_woe = sc.woebin_ply(test, bins)
#train_woe.head()

y_train = train_woe.loc[:,'status']
X_train = train_woe.loc[:, train_woe.columns != 'status']
y_test = test_woe.loc[:, 'status']
X_test = test_woe.loc[:, train_woe.columns != 'status']

lr = LogisticRegression(penalty='l1', C=0.9, solver='saga', n_jobs=-1)
lr.fit(X_train, y_train)

train_pred = lr.predict_proba(X_train)[:, 1]
test_pred = lr.predict_proba(X_test)[:, 1]

#训练集
proba_range = np.arange(0.2,0.9,0.01)
#print(proba_range)
for i in proba_range:
    i = round(i,2)
    train_pred_new = np.array(pd.DataFrame(train_pred).iloc[:, 0].apply(lambda x: 0 if x<i else 1))
    cm =confusion_matrix(y_train, train_pred_new)
    TPR = round(cm[0,0]/(cm[0,0]+cm[0,1]),4)
    FPR = round(cm[1,0]/(cm[1,0]+cm[1,1]),4)
    ks = round(TPR - FPR,4)
    #dpd_rate = round(cm[1,0]/(cm[0,0]+cm[1,0]),4)
    acc = round((cm[0,0]+cm[1,1])/cm.sum(),4)
    print(i, TPR, FPR, ks, acc)

#测试集
#test_pred_new = np.array(pd.DataFrame(test_pred).iloc[:, 0].apply(lambda x: 0 if x<0.35 else 1))
proba_range = np.arange(0.2,0.9,0.01)
#print(proba_range)
print('阈值', '真正率', '假正率', 'ks', '准确率')
for i in proba_range:
    i = round(i,2)
    test_pred_new = np.array(pd.DataFrame(test_pred).iloc[:, 0].apply(lambda x: 0 if x<i else 1))
    cm =confusion_matrix(y_test, test_pred_new)
    TPR = round(cm[0,0]/(cm[0,0]+cm[0,1]),4)
    FPR = round(cm[1,0]/(cm[1,0]+cm[1,1]),4)
    ks = round(TPR - FPR,4)
    #dpd_rate = round(cm[1,0]/(cm[0,0]+cm[1,0]),4)
    acc = round((cm[0,0]+cm[1,1])/cm.sum(),4)
    dpd = round(cm[1,0]/(cm[0,0]+cm[1,0]),4)
    print(i, TPR, FPR, ks, acc, dpd)


train_perf = sc.perf_eva(y_train, train_pred, title='train')
test_perf = sc.perf_eva(y_test, test_pred, title='test')

#保存模型
joblib.dump(lr, 'insight.m')
import sys
sys.path.append('./learn')

# from learn_ann import get_learner_params_all
from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split

import tensorflow as tf
K = tf.keras.backend

from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import auc
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
LW = 1.5 # line width for plots
LL = "lower right" # legend location
LC = 'darkgreen' # Line Color

# If you get error like ModuleNotFoundError: No module named 'tensorflow.keras',
# change line 2 to "K = tf.keras.backend"
# 
# https://www.kaggle.com/c/invasive-species-monitoring/discussion/32762
def AUC(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    K.get_session().run(tf.local_variables_initializer())
    return auc

DIR = './organized_dataset/'

seed = 7
np.random.seed(seed)

df = pd.read_csv(DIR+'feature_engineered_full.csv',header=0)
df_35 = pd.read_csv(DIR+'sorted_35_full.csv',header=0)

df = df.iloc[:df.shape[0]//2,:]
df_35 = df_35.iloc[:df_35.shape[0]//5,:]

print('Data loading Done')
print(df.describe())

col_max_value = df.iloc[:,4:-1].max()
col_min_value = df.iloc[:,4:-1].min()

df.iloc[:,4:-1] = (df.iloc[:,4:-1] - col_min_value) / (col_max_value - col_min_value)
df.fillna(0, inplace=True)

df_35.iloc[:,4:-1] = (df_35.iloc[:,4:-1] - col_min_value) / (col_max_value - col_min_value)
df_35.fillna(0, inplace=True)

print('Done')

from sklearn.tree import DecisionTreeClassifier

raw_data = df.iloc[:,3:-1].values
labels = df.iloc[:,-1].values

auc_list = []
auc_sk_list = []
fn_rate_list = []
fp_rate_list = []
num_of_folds = 10 ## k of k-fold cv ##

for k_index in range(num_of_folds):
    print('================ %d/%d th Learning ================'%(k_index+1,num_of_folds))
    X_train , X_test , y_train , y_test = train_test_split(raw_data , labels , test_size = 0.2,shuffle=True)
    
    temp = class_weight.compute_class_weight('balanced',np.unique(y_train),y_train)
    my_class_weight = {0:temp[0],1:temp[1]}
    print('class weight:',my_class_weight)

    model = DecisionTreeClassifier(class_weight = my_class_weight)
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)[:,1]
    
    tn, fp, fn, tp = confusion_matrix(np.where(y_pred > 0.3, 1, 0), y_test).ravel()
    fp_rate = float(fp)/float(fp+tn)
    fn_rate = float(fn)/float(tp+fn)
    fp_rate_list.append(fp_rate)
    fn_rate_list.append(fn_rate)
    print('False Positive Rate: %.5f'%(fp_rate))
    print('False Negative Rate: %.5f'%(fn_rate))
    
    fpr, tpr, th = roc_curve(y_test, y_pred)
    auc_sk = auc(fpr, tpr)
    auc_sk_list.append(auc_sk)
    print('AUC: %.5f'%(auc_sk))

    plt.figure()
    plt.title('%d/%d th TEST AUC: %f.5f'%(k_index+1,num_of_folds,auc_sk))
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('FALSE Positive Rate')
    plt.ylabel('TRUE Positive Rate')
    plt.plot(fpr, tpr, color=LC,lw=LW, label='ROC curve (area = %0.2f)' % auc_sk)
    plt.plot([0, 1], [0, 1], color='navy', lw=LW, linestyle='--') # reference line for random classifier
    plt.legend(loc=LL)
    plt.show()

print('================ Result ================')
temp = np.mean(auc_sk_list)
print('OVERALL TEST AUC Sk-learn: %.5f (+/- %.4f)'%(temp,np.std(auc_sk_list)))
print('False Positive Rate: %.5f (+/- %.4f)'%(np.mean(fp_rate_list),np.std(fp_rate_list)))
print('False Negative Rate: %.5f (+/- %.4f)'%(np.mean(fn_rate_list),np.std(fn_rate_list)))
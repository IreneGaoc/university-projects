import numpy as np
import pandas as pd
import sys, time

from sklearn import svm
from sklearn.linear_model import LogisticRegression


DIR = './organized_dataset/'

NUM_FEATURES = -1

def get_learner_params(df):
	N = df.shape[0]
	print('N: ',N)
	num_train = int(N*0.8)

	X_train = df.iloc[:num_train,3:NUM_FEATURES].values
	y_train = df.iloc[:num_train,NUM_FEATURES].values

	X_test = df.iloc[num_train:,3:NUM_FEATURES].values
	y_test = df.iloc[num_train:,NUM_FEATURES].values
	
	return X_train, y_train, X_test, y_test

def get_learner_testable_params(df):
	N = df.shape[0]
	num_train = int(N*0.8)

	X_train = df.iloc[:num_train,3:]
	# y_train = df.iloc[:num_train,-1]

	X_test = df.iloc[num_train:,3:]
	# y_test = df.iloc[num_train:,-1]

	# default
	X_train_1 = X_train.loc[X_train['STATUS'] == 1,'PREV_STATUS':'NEW_FEATURE_99']
	y_train_1 = X_train.loc[X_train['STATUS'] == 1,'STATUS']
	X_test_1 = X_test.loc[X_test['STATUS'] == 1,'PREV_STATUS':'NEW_FEATURE_99']
	y_test_1 = X_test.loc[X_test['STATUS'] == 1,'STATUS']

	# non-default
	X_train_0 = X_train.loc[X_train['STATUS'] == 0,'PREV_STATUS':'NEW_FEATURE_99']
	y_train_0 = X_train.loc[X_train['STATUS'] == 0,'STATUS']
	X_test_0 = X_test.loc[X_test['STATUS'] == 0,'PREV_STATUS':'NEW_FEATURE_99']
	y_test_0 = X_test.loc[X_test['STATUS'] == 0,'STATUS']

	temp = {1:(X_train_1, y_train_1, X_test_1, y_test_1), 0:(X_train_0, y_train_0, X_test_0, y_test_0)}

	return temp

def learn_svm(X_train, y_train, X_test, y_test):
	print('SVM')
	model = svm.SVC(kernel='linear', class_weight='balanced',verbose=True)
	# model = svm.SVC(kernel='linear',class_weight={0:6/1000, 1:1})
	model.fit(X_train, y_train)

	return model

def learn_logistic(X_train, y_train, X_test, y_test):
	print('Logistic Regression')
	model = LogisticRegression(random_state=0, solver='lbfgs',class_weight='balanced',verbose=0,max_iter=150)
	# model = LogisticRegression(random_state=0, solver='lbfgs',class_weight={0:6/1000, 1:1})
	model.fit(X_train, y_train)

	return model

def accuracy(model, test_params):

	# default
	X_train = test_params[1][0]
	y_train = test_params[1][1]
	X_test = test_params[1][2]
	y_test = test_params[1][3]
	y_pred_train = model.predict(X_train)
	y_pred_test = model.predict(X_test)

	accuracy_train = np.sum(y_train == y_pred_train) / len(y_train)
	accuracy_test = np.sum(y_test == y_pred_test) / len(y_test)

	print('=== Default Prediction Accuracy ===')
	print('train:',accuracy_train)
	print('test:',accuracy_test)

	# non-default
	X_train = test_params[0][0]
	y_train = test_params[0][1]
	X_test = test_params[0][2]
	y_test = test_params[0][3]
	y_pred_train = model.predict(X_train)
	y_pred_test = model.predict(X_test)

	accuracy_train = np.sum(y_train == y_pred_train) / len(y_train)
	accuracy_test = np.sum(y_test == y_pred_test) / len(y_test)

	print('=== Non-Default Prediction Accuracy ===')
	print('train:',accuracy_train)
	print('test:',accuracy_test)


def main():

	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('Start: %s\n'%(current_time_str) )

	if len(sys.argv) > 1:
		if sys.argv[1] == 'full':
			df = pd.read_csv(DIR+'feature_engineered_full.csv')
		elif sys.argv[1] == 'test':
			df = pd.read_csv(DIR+'feature_engineered_test.csv')
		else:
			df = pd.read_csv(DIR+'feature_engineered_head.csv')
	else:
		df = pd.read_csv(DIR+'feature_engineered_head.csv')

	X_train, y_train, X_test, y_test = get_learner_params(df)
	test_params = get_learner_testable_params(df)

	# svm_model = learn_svm(X_train, y_train, X_test, y_test)
	# print('train score:',svm_model.score(X_train, y_train))
	# print('test score:',svm_model.score(X_test, y_test))
	# print('train 2 score: ',svm_model.score(X_train_2,y_train_2))
	# print('test 2 score: ',svm_model.score(X_test_2,y_test_2))

	# accuracy(svm_model, X_train_2, y_train_2, X_test_2, y_test_2)


	lr_model = learn_logistic(X_train, y_train, X_test, y_test)
	print('train score:',lr_model.score(X_train, y_train))
	print('test score:',lr_model.score(X_test, y_test))

	accuracy(lr_model, test_params)

	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('\nEnd: %s\n'%(current_time_str) )

if __name__ == '__main__':
	main()
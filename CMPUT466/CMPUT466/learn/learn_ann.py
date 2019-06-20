import tensorflow as tf
from tensorflow import keras
from metric_auc import auc

import pandas as pd
import sys, time

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



def learn(X_train,y_train, X_test, y_test):

	M = X_train.shape[1]

	model = keras.Sequential()

	model.add(keras.layers.Dense(M, input_dim=M, kernel_initializer='normal', activation='sigmoid'))
	model.add(keras.layers.Dense(M//2, kernel_initializer='normal', activation='relu'))
	model.add(keras.layers.Dense(1, kernel_initializer='normal', activation='sigmoid'))

	model.compile(optimizer='adam', 
				  loss='binary_crossentropy',
				  metrics=[auc])

	model.fit(X_train, y_train, epochs=5)

	train_loss, train_auc = model.evaluate(X_train, y_train)
	test_loss, test_auc = model.evaluate(X_test, y_test)

	print('Train Loss:',train_loss)
	print('Train AUC:', train_auc)

	print('Test Loss:',test_loss)
	print('Test AUC:', test_auc)


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

	learn(X_train, y_train, X_test, y_test)

	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('\nEnd: %s\n'%(current_time_str) )

if __name__ == '__main__':
	main()
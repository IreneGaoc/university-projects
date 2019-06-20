import sys, time
# sys.path.append('./learn')

from tensorflow import keras
import pandas as pd
import numpy as np
import tensorflow as tf
K = tf.keras.backend


DIR = '../organized_dataset/'
SHORT_TERM = 6

seed = 7
np.random.seed(seed)

df = pd.read_csv(DIR+'feature_engineered_test.csv',header=0)
df_35 = pd.read_csv(DIR+'sorted_35_test.csv',header=0)

print('Data loading Done')

BATCH_SIZE = 100

NUM_OF_FEATURES = df.iloc[0,3:-1].count()
# NUM_OF_FEATURE = 40
INDEX_OF_LAST_FEATURE = NUM_OF_FEATURES + 3
SEQUENCE_LENGTH = SHORT_TERM


def retrieve_long_term():
	global df, df_35

	print('Term: ',SHORT_TERM)

	temp = df.groupby('CID').count()
	temp.rename(columns={temp.columns[0]:'length'}, inplace=True)

	# get as Series of CID with contract-length less than SHORT_TERM
	# temp = temp.loc[temp['length'] >= SHORT_TERM].iloc[:,0]
	temp = temp.loc[temp['length'] < SHORT_TERM].iloc[:,0]
	print('# of short-term CID: ',temp.shape[0])

	short_cid_set = set(temp.index.tolist())

	# remove short-term customers
	for cid in short_cid_set:
		df.drop(df[df['CID']==cid].index, inplace=True)

	long_df = df
	print('dataset: ',long_df.shape)
	temp = long_df.groupby('CID').count()
	temp.rename(columns={temp.columns[0]:'length'}, inplace=True)
	temp = temp.loc[temp['length'] >= SHORT_TERM].iloc[:,0]
	print('# of long-term CID: ',temp.shape[0])
	# print('Done')

def get_dict_dfs(df,short_term=6):
	global df_35
	dict_of_df = {}
  
	length_df = df.groupby('CID').count()
	length_df.rename(columns={length_df.columns[0]:'length'}, inplace=True)

	# exclude 35-months customers.
	for length in range(short_term,35):
		print('Processing length:',length)
		temp = length_df[length_df['length'] == length]
		short_cid_list = set(temp.index.values)

		current_df = pd.DataFrame(columns=df.columns)
		for cid in short_cid_list:
			temp = df.loc[df['CID']==cid].sort_values(by='DATE')
			current_df = current_df.append(temp, ignore_index=True)

		dict_of_df[length] = current_df
	
	# For 35-months customers
	length = 35
	print('For length:',length)
	dict_of_df[length] = df_35

	return dict_of_df

#### get next training batch of customers with 35 months contract
def next_train_batch_35(dict_dfs,num_of_features,index_of_last_feature,sequence_length,k=10,test_start_idx=0):
	if test_start_idx<0 or test_start_idx>=k:
		raise Exception("test_start_idx (%d) should be in range(0,k=%d)"%(test_start_idx,k))
	length = 35
	
	end = dict_dfs[length].shape[0]
	temp = int(end*(test_start_idx/k))
	test_start = temp - (temp % length)
	temp = int(end*((test_start_idx+1)/k))
	test_end = temp - (temp % length)
	
	df = dict_dfs[length].iloc[:test_start,:].append(dict_dfs[length].iloc[test_end:,:])
	end = df.shape[0]
	
	temp_index_list = [list(range(i,i+sequence_length)) for i in range(0,end-sequence_length+1,length)]
	batch_size = len(temp_index_list)
	yield end, batch_size
	
	while True:
		for start in range(0,length-sequence_length+1):
			temp_index_list = [list(range(i,i+sequence_length)) for i in range(start,end-sequence_length+1,length)]
			batch_size = len(temp_index_list)

			X = np.zeros((batch_size,sequence_length,num_of_features))
			y = np.zeros((batch_size,1))

			for b in range(0,batch_size):
				X[b,:,:] = df.iloc[temp_index_list[b],3:index_of_last_feature].values
				y[b,0] = df.iloc[temp_index_list[b][-1],-1]

			yield X,y.astype(int)

#### get next test batch of customers with 35 months contract
def next_test_batch_35(dict_dfs,num_of_features,index_of_last_feature,sequence_length,k=10,test_start_idx=0,):
	if test_start_idx<0 or test_start_idx>=k:
		raise Exception("test_start_idx (%d) should be in range(0,k=%d)"%(test_start_idx,k))
	
	length = 35
	end = dict_dfs[length].shape[0]
	temp = int(end*(test_start_idx/k))
	test_start = temp - (temp % length)
	temp = int(end*((test_start_idx+1)/k))
	test_end = temp - (temp % length)
	
	df = dict_dfs[length].iloc[test_start:test_end,:]
	end = df.shape[0]
	
	temp_index_list = [list(range(i,i+sequence_length)) for i in range(0,end-sequence_length+1,length)]
	batch_size = len(temp_index_list)
	
	yield end, batch_size
	
	while True:
		for start in range(0,length-sequence_length+1):
			temp_index_list = [list(range(i,i+sequence_length)) for i in range(start,end-sequence_length+1,length)]
			batch_size = len(temp_index_list)

			X = np.zeros((batch_size,sequence_length,num_of_features))
			y = np.zeros((batch_size,1))

			for b in range(0,batch_size):
				X[b,:,:] = df.iloc[temp_index_list[b],3:index_of_last_feature].values
				y[b,0] = df.iloc[temp_index_list[b][-1],-1]

			yield X,y.astype(int)

def next_train_batch(dict_dfs,num_of_features,index_of_last_feature,sequence_length,k=10,test_start_idx=0):
	if test_start_idx<0 or test_start_idx>=k:
		raise Exception("test_start_idx (%d) should be in range(0,k=%d)"%(test_start_idx,k))
	
	while True:
		for length in range(sequence_length,36):
			end = dict_dfs[length].shape[0]
			temp = int(end*(test_start_idx/k))
			test_start = temp - (temp % length)
			temp = int(end*((test_start_idx+1)/k))
			test_end = temp - (temp % length)

			df = dict_dfs[length].iloc[:test_start,:].append(dict_dfs[length].iloc[test_end:,:])
			end = df.shape[0]
			
			for start in range(0,length-sequence_length+1):
				temp_index_list = [list(range(i,i+sequence_length)) for i in range(start,end-sequence_length+1,length)]
				batch_size = len(temp_index_list)

				X = np.zeros((batch_size,sequence_length,num_of_features))
				y = np.zeros((batch_size,1))
			
				for b in range(0,batch_size):
					X[b,:,:] = df.iloc[temp_index_list[b],3:index_of_last_feature].values
					y[b,0] = df.iloc[temp_index_list[b][-1],-1]

				yield X,y.astype(int)

def next_test_batch(dict_dfs,num_of_features,index_of_last_feature,sequence_length,k=10,test_start_idx=0):
	if test_start_idx<0 or test_start_idx>=k:
		raise Exception("test_start_idx (%d) should be in range(0,k=%d)"%(test_start_idx,k))
	
	while True:
		for length in range(sequence_length,36):
			end = dict_dfs[length].shape[0]
			temp = int(end*(test_start_idx/k))
			test_start = temp - (temp % length)
			temp = int(end*((test_start_idx+1)/k))
			test_end = temp - (temp % length)

			df = dict_dfs[length].iloc[test_start:test_end,:]
			end = df.shape[0]
			
			for start in range(0,length-sequence_length+1):
				temp_index_list = [list(range(i,i+sequence_length)) for i in range(start,end-sequence_length+1,length)]
				batch_size = len(temp_index_list)

				X = np.zeros((batch_size,sequence_length,num_of_features))
				y = np.zeros((batch_size,1))
			
				for b in range(0,batch_size):
					X[b,:,:] = df.iloc[temp_index_list[b],3:index_of_last_feature].values
					y[b,0] = df.iloc[temp_index_list[b][-1],-1]

				yield X,y.astype(int)

def auc(y_true, y_pred):
	# https://stackoverflow.com/questions/48174323/tensorflow-1-4-tf-metrics-auc-for-auc-calculation
	auc_temp = tf.metrics.auc(y_true, y_pred)[1]
	K.get_session().run(tf.local_variables_initializer())
	return auc_temp

def learn(dict_dfs,num_of_folds=5):
	cv_list = []     ## store cross-validation scores ##
	for k_index in range(num_of_folds):
		print('================ %d/%d th Learning ================'%(k_index+1,num_of_folds))
		train_batch_generator = next_train_batch_35(dict_dfs,
												num_of_features = NUM_OF_FEATURES,
												index_of_last_feature=INDEX_OF_LAST_FEATURE,
												sequence_length=SEQUENCE_LENGTH,
												k=num_of_folds,
												test_start_idx=k_index)
		test_batch_generator = next_test_batch_35(dict_dfs,
												num_of_features = NUM_OF_FEATURES,
												index_of_last_feature=INDEX_OF_LAST_FEATURE,
												sequence_length=SEQUENCE_LENGTH,
												k=num_of_folds,
												test_start_idx=k_index)

		train_size, train_batch_size = next(train_batch_generator)
		test_size, test_batch_size = next(test_batch_generator)

		print(df.shape)
		print('X_train: ',train_size)
		print('train batch: ',train_batch_size)
		print('X_test: ',test_size)
		print('test batch: ',test_batch_size)
	  
		model = keras.Sequential()
		model.add(keras.layers.LSTM(50, batch_input_shape=(None, SEQUENCE_LENGTH, NUM_OF_FEATURES),stateful=False,activation='relu'))
		model.add(keras.layers.BatchNormalization())
		model.add(keras.layers.Dense(32,kernel_initializer='normal', activation='relu'))
		model.add(keras.layers.Dense(1,kernel_initializer='normal', activation='sigmoid'))

		model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[auc])

		#### fit model with next train batch ####
		model.fit_generator(generator=train_batch_generator, 
							steps_per_epoch=100, epochs=30, verbose=1, 
							class_weight = {0: 1,1: 33})
		
		#### evaluate model by next test batch ####
		result = model.evaluate_generator(generator=test_batch_generator, steps=int(test_size/test_batch_size))
		print('%d/%d th TEST AUC: %.5f'%(k_index+1,num_of_folds,result[1]))
		cv_list.append(result[1])

	print('================ Result ================')
	print('OVERALL TEST AUC: %.5f (+/- %.4f)'%(np.mean(cv_list),np.std(cv_list)))

def main():
	print(df.describe())

	col_max_value = df.iloc[:,4:-1].max()
	col_min_value = df.iloc[:,4:-1].min()

	df.iloc[:,4:-1] = (df.iloc[:,4:-1] - col_min_value) / (col_max_value - col_min_value)
	df.fillna(0, inplace=True)

	df_35.iloc[:,4:-1] = (df_35.iloc[:,4:-1] - col_min_value) / (col_max_value - col_min_value)
	df_35.fillna(0, inplace=True)
	retrieve_long_term()
	dict_dfs = get_dict_dfs(df,short_term = SHORT_TERM)
	learn(dict_dfs,5)


if __name__ == '__main__':
	main()
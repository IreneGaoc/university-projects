import pandas as pd
from sqlalchemy import create_engine
import time, datetime, sys
import numpy as np
from sklearn import linear_model


# To ignore harmless warning
import warnings
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

DIR = './organized_dataset/'

DEFAULT_FEATURES = ['GLOBAL_ID','CID','DATE','STATUS','N_CR_ABM','N_CR_BRCH','N_CR_CHQ','N_CR_EFT','N_CR_MOBILE','N_CR_ONLINE','N_CR_OTHER','N_CR_PE','N_CR_POS','N_DB_ABM','N_DB_BRCH','N_DB_CHQ','N_DB_EFT','N_DB_MOBILE','N_DB_ONLINE','N_DB_OTHER','N_DB_PE','N_DB_POS','V_CR_ABM','V_CR_BRCH','V_CR_CHQ','V_CR_EFT','V_CR_MOBILE','V_CR_ONLINE','V_CR_OTHER','V_CR_PE','V_CR_POS','V_DB_ABM','V_DB_BRCH','V_DB_CHQ','V_DB_EFT','V_DB_MOBILE','V_DB_ONLINE','V_DB_OTHER','V_DB_PE','V_DB_POS']

NUM_OF_INDEPENDENT = len(DEFAULT_FEATURES) - 3 # exclude GLOBAL_ID, CID, DATE

NUM_OF_FEATURE = 100

NUM_OF_CUSTMERS_LIMIT = 2000

class DataManager:
	def __init__(self):
		self.engine = create_engine('sqlite://', echo=False)
		self.dataframe_profile = None
		self.dataframe_transactions = None
		self.dataframe_dependent = None
		self.df_full = None


		self.dataframe_A = None
		self.dataframe_y = None

	def read_csv(self,filepath,table_name):
		df = pd.read_csv(filepath,header=0)
		df.to_sql(table_name,self.engine)
		return df

	def read_profile(self,filepath):
		self.dataframe_profile = self.read_csv(filepath, table_name='profile')

	def read_transactions(self,filepath):
		self.dataframe_transactions = self.read_csv(filepath, table_name='transactions')

	def read_dependent(self,filepath):
		self.dataframe_dependent = self.read_csv(filepath, table_name='dependent')

	def read_full(self,filepath):
		print('loading full csv')
		self.df_full = pd.read_csv(filepath,header=0)
		print('loaded %s and created DataFrame'%(filepath))

	def read_full_head(self,filepath):
		print('loading head csv')
		self.df_full = pd.read_csv(filepath,header=0)
		print('loaded %s and created DataFrame'%(filepath))

	def read_test(self,filepath):
		print('loading test csv')
		self.df_full = pd.read_csv(filepath,header=0)
		print('loaded %s and created DataFrame'%(filepath))

"""
	Count some stats of dataset
	- total rows: 1266792
	- # of default: 39015
	- ratio: 0.030798268381865373
	- # of customers: 41326
"""
def count(df):
	num = len(list(df.iloc[:,0]))
	num_of_default = len(list(df.loc[df['STATUS'] == 1,'CID']))
	num_of_customer = len(set(df.loc[:,'CID']))

	print('total rows: ',num)
	print('# of default: ',num_of_default)
	print('ratio: ',num_of_default/num)
	print('# of customers: ',num_of_customer)

"""
	Feature selection for each customer
	@ndarray feature[first_month:last_month, DATE:end] of one customer
"""
def compress_feature(ndarray):

	np.set_printoptions(threshold=sys.maxsize)

	extended_array = np.zeros((ndarray.shape[0], NUM_OF_FEATURE))
	extended_array[:,0:ndarray.shape[1]] = ndarray.copy()

	# flag = False
	# if 1 in list(ndarray[:,3]):

	# 	print(ndarray[:,3])
	# 	print('')
	# 	print(extended_array[:,3])
	# 	print('')
	# 	print('')
	# 	# exit()
	# 	flag = True

	# next empty column
	next_empty = ndarray.shape[1]

	if len(ndarray) == 1:
		A = extended_array[:,:]
		b = ndarray[:,3]
		return A, b

	# index_global_id = 0
	# index_cid = 1
	# index_date = 2
	index_status = 3



	for month in range(1,len(ndarray)):
		# next empty column
		next_empty = ndarray.shape[1]

		##### FEATURE 1: previous month status
		extended_array[month,index_status] = ndarray[month-1,index_status]

		##### FEATURE 35(next_empty): linear regression (1-deg) of STATUS
		b = ndarray[:month,index_status]
		B = np.ones((len(b),2))
		for r in range(len(b)):
			B[r,1] = r

		model = linear_model.LinearRegression()
		model.fit(B,b)

		# Add slope of regression as feature
		extended_array[month,next_empty] = model.coef_[1]


		# partition features into two
		feature_index_0 = index_status+1		# N_CR_ABM
		feature_index_1 = DEFAULT_FEATURES.index('N_DB_POS')

		next_empty += 1

		##### FEATURES (1d LR of num of tx)
		for feature_index in range(feature_index_0,feature_index_1+1):
			b = ndarray[:month,feature_index]
			B = np.ones((len(b),2))
			for r in range(len(b)):
				B[r,1] = r

			model = linear_model.LinearRegression()
			model.fit(B,b)

			# Add slope of regression as feature
			extended_array[month,next_empty] = model.coef_[1]
			next_empty += 1

		##### FEATURES (avg of $ amount, LR of $ amount)
		for feature_index in range(feature_index_1+1,len(DEFAULT_FEATURES)):
			mean = ndarray[:month,feature_index].mean()
			extended_array[month,next_empty] = mean
			next_empty += 1

			b = ndarray[:month,feature_index]
			B = np.ones((len(b),2))
			for r in range(len(b)):
				B[r,1] = r

			model = linear_model.LinearRegression()
			model.fit(B,b)

			# Add slope of regression as feature
			extended_array[month,next_empty] = model.coef_[1]
			next_empty += 1

	# if flag:
	# 	print(ndarray[:,3])
	# 	print('')
	# 	print(extended_array[:,3])
	# 	exit()

	return extended_array, ndarray[:,index_status]

# def create_A_b_lineByline(df, mode):
# 	temp = df.values
# 	N = temp.shape[0]
# 	M = temp.shape[1]

# 	extended_array = np.zeros((N,NUM_OF_FEATURE))
# 	b = np.zeros((N))

# 	extended_array[:,:M] = temp

# 	# print(extended_array.shape)
# 	# print(extended_array[:4,:5])

# 	start = 0
# 	current_cid = extended_array[0,1]
# 	count = 0
# 	for row in range(1,N):
# 		next_cid = extended_array[row,1]
# 		if next_cid != current_cid:
# 			_A, _b = compress_feature(extended_array[start:row,:M])
# 			extended_array[start:row,:] = _A
# 			b[start:row] = _b
# 			start = row
# 			current_cid = next_cid

# 			if count % (42000//1000+1) == 0:
# 				print('%d th CID done'%(count))

# 			# if test, limit exists.
# 			if count > NUM_OF_CUSTMERS_LIMIT and mode == 2:
# 				break

# 			count += 1

# 	return extended_array, b

def create_A_b(df, mode):
	# set of all customer id (CID)
	cid_set = set(df.loc[:,'CID'])
	print('# of CID: ',len(cid_set))

	# https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
	A = np.array([[1]*NUM_OF_FEATURE])
	b = np.array([1])

	count = 0
	for cid in cid_set:
		# https://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array
		ndarray = df.loc[df['CID']==cid,:].values
		# print(ndarray[:,:5])
		# print('')

		A_new, b_new = compress_feature(ndarray)

		A = np.concatenate((A,A_new))
		b = np.concatenate((b,b_new))

		if count % (len(cid_set)//1000+1) == 0:
			print('%d th CID done: %s'%(count, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) ) )

		# if test, limit exists.
		if count > NUM_OF_CUSTMERS_LIMIT and mode == 2:
			break

		count+=1

	# print('=====================')
	# for i in range(1,A.shape[0]):
	# 	print(A[i,:5])
	# 	print(b[i])
	# exit()

	print('All CID done: %d, %s'%(count, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) ))
	return A[1:,:], b[1:]

def create_csv(df,A,b,mode):
	# N = A.shape[0]
	# if mode == 2:
	# 	# df = df.iloc[:N,:]
	# 	df.drop(df.index[N:],inplace=True)

	# print('=====================')
	# for i in range(0,A.shape[0]):
	# 	# temp = list(np.int_(A[i,:]))
	# 	# if 3240 in temp or 3776 in temp:
	# 	print(A[i,:7])
	# 	print(b[i])

	# print(df.loc[df['CID']==133240].iloc[:,:5])
	# print(df.loc[df['CID']==133776].iloc[:,:5])


	df.rename(columns = {'STATUS':'PREV_STATUS'}, inplace = True)

	columns = list(df.columns.values)
	for col in range(len(DEFAULT_FEATURES),A.shape[1]):
		columns.append('NEW_FEATURE_'+str(col))
	# columns.append('STATUS')

	print('=====================')
	# print(columns)

	final_df = pd.DataFrame(data=A,columns = columns)
	final_df['CID'] = np.int_(A[:,1])
	final_df['DATE'] = A[:,2]
	final_df['PREV_STATUS'] = np.int_(A[:,3])
	final_df['STATUS'] = np.int_(b)

	print(final_df.columns)

	# print('======================')
	# print(final_df.loc[final_df['CID']==133240].iloc[:,:5])
	# print(final_df.loc[final_df['CID']==133776].iloc[:,:5])
	# print('======================')
	# print(final_df.loc[final_df['CID']==133240].iloc[:,-3:])
	# print(final_df.loc[final_df['CID']==133776].iloc[:,-3:])

	print(final_df.info())

	# df['PREV_STATUS'] = np.int_(A[:,3])
	# print(np.int_(A[:,3]))

	# for col in range(len(DEFAULT_FEATURES),A.shape[1]):
	# 	df['NEW_FEATURE_'+str(col)] = A[:,col]

	# df['STATUS'] = np.int_(b)
	# print(np.int_(b))

	A = A[:,3:]

	if mode == 1:
		final_df.iloc[:,1:].to_csv(DIR+'feature_engineered_full.csv')
	elif mode == 2:
		final_df.iloc[:,1:].to_csv(DIR+'feature_engineered_test.csv')
	else:
		final_df.iloc[:,1:].to_csv(DIR+'feature_engineered_head.csv')

def stats(df):
	cid_set = set(df.loc[:,'CID'])
	print('# of CID: ',len(cid_set))

	count_dict = {}
	for cid in cid_set:
		c = df.groupby(cid).count()
		if c in count_dict.keys():
			count_dict[c] += 1
		else:
			count_dict[c] = 1

	print(count_dict)

def main():
	global NUM_OF_FEATURE
	manager = DataManager()

	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('Start: %s\n'%(current_time_str) )

	# 0: head, 1: full, 2: test
	mode = 0

	if len(sys.argv) > 1:
		if sys.argv[1] == 'full':
			manager.read_full(DIR+'full.csv')
			mode = 1
		elif sys.argv[1] == 'test':
			print('test feature selections.')
			manager.read_full(DIR+'full.csv')
			mode = 2
		else:
			manager.read_full_head(DIR+'full_head.csv')
	else:
		manager.read_full_head(DIR+'full_head.csv')

	print('NUM_OF_DEFAULT_FEATURES:',len(DEFAULT_FEATURES))
	print('NUM_OF_INDEPENDENT:',NUM_OF_INDEPENDENT)

	count(manager.df_full)
	# A, b = create_A_b_lineByline(manager.df_full, mode)
	A, b = create_A_b(manager.df_full, mode)

	print('A: ',A.shape)
	print('b: ',b.shape)

	create_csv(manager.df_full,A, b,mode)

	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('created CSV: %s'%(current_time_str) )
	
	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('\nEnd: %s\n'%(current_time_str) )



if __name__ == '__main__':
	main()
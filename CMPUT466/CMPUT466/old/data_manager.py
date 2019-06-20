import pandas as pd
from sqlalchemy import create_engine
import time
import datetime
import numpy as np
from sklearn import linear_model

# To ignore harmless warning
import warnings
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

DIR = './dataset/'

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
		self.df_full = self.read_csv(filepath, table_name='full')
		print('full.csv loaded')

	def read_full_light(self,filepath):
		print('loading csv')
		self.df_full = pd.read_csv(filepath,header=0)
		print('loaded csv and created DataFrame')


	def get_profile(self,cid):
		tuples = self.engine.execute('select * from profile p where p.CUST_OID = %d'%(cid)).fetchall()
		return tuples

	def get_all_transactions(self,cid):
		tuples = self.engine.execute('select * from transactions tx where tx.CID = %d'%(cid)).fetchall()
		return tuples

	"""
		As of @year, @month, get the most recent @month_period months of tx records of customer of @cid 

		@return (dataframe, list): return found row in two formats; dataframe and list.
	"""
	def get_recent_transactions(self,cid,year_upto,month_upto,month_period=12):
		
		# end date
		date_obj_upto = datetime.date(year_upto, month_upto, 1)
		date_upto = time.mktime(date_obj_upto.timetuple())

		# start date
		year_from = year_upto
		month_from = month_upto - month_period

		if month_from < 0:
			year_from -= -(month_from // 12)
			month_from = month_from % 12
			if month_from == 0:
				month_from = 12
				year_from -= 1
		elif month_from == 0:
			year_from -= 1
			month_from = 12


		date_obj_from = datetime.date(year_from, month_from, 1)
		date_from = time.mktime(date_obj_from.timetuple())
		tuples = self.engine.execute('select * from transactions tx where tx.CID = %d and tx.TRANSACTED_ON >= %f and tx.TRANSACTED_ON < %f'%(cid,date_from,date_upto)).fetchall()

		temp_list = [list(each)[1:] for each in tuples]
		

		# https://stackoverflow.com/questions/33700626/how-to-convert-tuple-of-tuples-to-pandas-dataframe-in-python
			# print(self.dataframe_transactions.columns)
			# print(len(self.dataframe_transactions.columns))
			# print(temp_list)
		df = pd.DataFrame(temp_list,columns = self.dataframe_transactions.columns)


		return df, temp_list


	def feature_engineering(self):
		# cid = 68028158
		# year_upto = 2019
		# month_upto = 2
		# month_period = 12
		# df, _ = self.get_recent_transactions(cid, year_upto, month_upto, month_period)
		# print(df)


		

		pass



	def get_learning_data(self):
		return 0,0,0,0

# feature selection for each customer
def compress_feature(ndarray):

	temp_array = np.zeros((ndarray.shape[0], 100))
	temp_array[:,0:ndarray.shape[1]] = ndarray.copy()

	# next empty column
	next_empty = ndarray.shape[1]

	if len(ndarray) == 1:
		A = ndarray[:,:]
		b = ndarray[:,1]
		return A, b

	for i in range(1,len(ndarray)):
		# A = ndarray[i:,:]
		# b = ndarray[i:,1]

		##### FEATURE 1: previous month status
		temp_array[i,1] = ndarray[i-1,1]

		##### FEATURE 35(next_empty): linear regression (1-deg) of STATUS
		b = ndarray[:i]
		B = np.ones((len(b),2))
		for r in range(len(b)):
			B[r,1] = r

		model = linear_model.LinearRegression()
		model.fit(B,b)

		# overwrite STATUS with slope of regression
		temp_array[i,next_empty] = model.coef_[1]


		##### FEATURE 36(next_empty+1): average






	return A,b

def main():
	manager = DataManager()
	manager.read_profile(DIR+'profile.csv')
	manager.read_transactions(DIR+'transactions.csv')

	# cid = 68028158
	# year_upto = 2019
	# month_upto = 2
	# month_period = 12
	# df, _ = manager.get_recent_transactions(cid, year_upto, month_upto, month_period)
	# print(df)

def main_full():
	manager = DataManager()
	manager.read_full_light(DIR+'full_head.csv')

	df = manager.df_full

	cid_set = set(df.loc[:,'CID'])
	print('# of cid: ',len(cid_set))

	# https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
	# print(df.loc[df['CID']==129670])

	for cid in cid_set:
		# https://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array
		ndarray = df.loc[df['CID']==cid,'DATE':].values
		# print(ndarray)
		A,b = compress_feature(ndarray)
		# print(A)
		# print(b)
		break


if __name__ == '__main__':
	# main()
	# test2()
	main_full()
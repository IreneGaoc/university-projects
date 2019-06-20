import pandas as pd
from sqlalchemy import create_engine
import time
import datetime


DIR = './dataset/'
MONTH = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

DEFAULT_DEPENDENT_FILE_NAME = 'Data_type_dependantvariable.csv'
DEFAULT_TX_FILE_NAME = 'Data_type_22.csv'
DEFAULT_PROFILE_FILE_NAME = 'Data_type_1.csv'
DEFAULT_FULLDATA1_FILE_NAME = 'T9_BUS_PTNR_TRXN.csv'

engine = create_engine('sqlite://', echo=False)



"""
- Edit csv file of dependent variable to useful format.
- Then create new file as 'dependent.csv'
"""
def organize_dependent(filepath):
	df = pd.read_csv(filepath,header=0)

	df['Month'] = df['Month'].apply(lambda x: to_datetime_1(x)[1])
	df['Value'] = df['Value'].apply(lambda x: 0 if x=='Current' else 1)

	df.to_csv(DIR+'dependent.csv')



"""
- Convert csv file of transactions record to useful format.
- Then create new file as 'transactions.csv'
"""
def organize_tx(filepath):
	df = pd.read_csv(filepath,header=0)

	# ---------------------------------------------------
	# EDIT #1
	# convert transaction's date into long
	df['TRANSACTED_ON'] = df['TRANSACTED_ON'].apply(lambda x: to_datetime_2(x)[1])
	df['TX_DATE'] = df['Transaction_date'].apply(lambda x: to_datetime_2(x)[1])

	df.drop(['Transaction_date'], axis=1, inplace=True)

	# ---------------------------------------------------
	# EDIT #2
	# convert transaction's account type into binary
	set_of_account_type = set(df.loc[:,'acct_type'].tolist())

	for account_type in set_of_account_type:
		df['ACT_TYP_'+account_type] = df['acct_type'].apply(lambda x: 1 if x==account_type else 0)

	df.drop(['acct_type'], axis=1, inplace=True)

	# ---------------------------------------------------
	# EDIT #3
	# convert transaction's category into binary
	set_of_category = set(df.loc[:,'CATEGORY'].tolist())

	for category in set_of_category:
		df['CAT_'+category] = df['CATEGORY'].apply(lambda x: 1 if x==category else 0)

	df.drop(['CATEGORY'], axis=1, inplace=True)

	# ---------------------------------------------------
	# EDIT #4
	# convert debit flag into binary
	# - Debit: 1, Credit: 0
	df['DEBIT'] = df['Debit_Credit_Flag'].apply(lambda x: 1 if x == 'DB' else 0)
	df.drop(['Debit_Credit_Flag'], axis=1, inplace=True)

	# ---------------------------------------------------
	# EDIT #5
	# convert debit/credit into binary
	# - Debit: 1, Credit: 0
	df['dbcr'] = df['trkit_dbcr'].apply(lambda x: 1 if x == 'DEBIT' else 0)
	df.drop(['trkit_dbcr'], axis=1, inplace=True)


	# ---------------------------------------------------
	# EDIT #6
	# We ignore Time
	df.drop(['Transaction_time'], axis=1, inplace=True)

	df.to_csv(DIR+'transactions.csv')


"""
- Translate Date format of (Jan-18) -> (1-Jan-18) -> long format (1351749600.0)
	@param str date_str: date string in MMM-YY
	@return tuple: (datetime object, long)
"""
def to_datetime_1(date_str):

	# if missing data
	if len(str(date_str)) < 4:
		# dummy date 2019/1/1 is set
		date_obj = datetime.date(2019, 1, 1)
		return date_obj, time.mktime(date_obj.timetuple())

	temp = date_str.split('-')
	y = 2000 + int(temp[1])
	m = 1 + MONTH.index(temp[0].upper())

	date_obj = datetime.date(y, m, 1)
	return date_obj, time.mktime(date_obj.timetuple())

"""
- Translate Date format of (1-Jan-18) into long format (1351749600.0)
	@param str date_str: date string in DD-MMM-YY
	@return tuple: (datetime object, long)
"""
def to_datetime_2(date_str):

	# if missing data
	if len(str(date_str)) < 4:
		# dummy date 2019/1/1 is set
		date_obj = datetime.date(2019, 1, 1)
		return date_obj, time.mktime(date_obj.timetuple())


	temp = date_str.split('-')

	y = 2000 + int(temp[2])
	m = 1 + MONTH.index(temp[1].upper())
	d = int(temp[0])

	date_obj = datetime.date(y, m, d)

	return date_obj, time.mktime(date_obj.timetuple())

"""
- Translate Date format of (Jan-18) into long format (1351749600.0)
	@param str date_str: date string in DD-MMM-YY
	@return tuple: (datetime object, long)
"""
def to_datetime_3(date_str):
	# if missing data
	if len(str(date_str)) < 4:
		# dummy date 2019/1/1 is set
		date_obj = datetime.date(2019, 1, 1)
		return date_obj, time.mktime(date_obj.timetuple())

	d = int(date_str[0:2])
	m = 1 + MONTH.index(date_str[2:5])
	y = int(date_str[5:len(date_str)])

	date_obj = datetime.date(y, m, d)

	return date_obj, time.mktime(date_obj.timetuple())


def organize_full(filepath):
	df_original = pd.read_csv(filepath,header=0)

	# ---------------------------------------------------
	# EDIT #1
	# convert transaction's date into long
	df_original['DATE'] = df_original['DATE'].apply(lambda x: to_datetime_3(x)[1])

	df_original['STATUS'] = df_original['STATUS'].apply(lambda x: 0 if x==1 else 1)

	df_original.rename(columns={'BUS_PTNR_OID':'CID'},inplace=True)

	df_original.to_csv(DIR+'full.csv')
	df_original.iloc[0:1000,:].to_csv(DIR+'full_head.csv')
	print('Done')



def test():
	d1 = to_datetime_1('Nov-12')
	d2 = to_datetime_2('9-Jan-19')

	print(d1) # (datetime.date(2012, 11, 1), 1351749600.0)
	print(d2) # (datetime.date(2019, 1, 9), 1547017200.0)

# for sample dataset
def organize():
	organize_dependent('./original_dataset/'+DEFAULT_DEPENDENT_FILE_NAME)
	organize_tx('./original_dataset/'+DEFAULT_TX_FILE_NAME)

# for full dataset
def organize2():
	organize_full('./original_dataset/'+DEFAULT_FULLDATA1_FILE_NAME)

def main():
	organize_dependent('./original_dataset/'+DEFAULT_DEPENDENT_FILE_NAME)
	organize_tx('./original_dataset/'+DEFAULT_TX_FILE_NAME)


if __name__ == '__main__':
	# main()
	# test()
	organize2()
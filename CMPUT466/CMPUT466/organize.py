import pandas as pd
from sqlalchemy import create_engine
import time
import datetime


DIR = './organized_dataset/'
MONTH = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

DEFAULT_FULLDATA1_FILE_NAME = 'T9_BUS_PTNR_TRXN.csv'

engine = create_engine('sqlite://', echo=False)


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
- Translate Date format of (DDMMMYYYY) into long format (1351749600.0)
	@param str date_str: date string in DDMMMYYYY
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
	print('Organizing...')
	df_original = pd.read_csv(filepath,header=0)

	# ---------------------------------------------------
	# EDIT #1
	# convert transaction's date into long
	df_original['DATE'] = df_original['DATE'].apply(lambda x: to_datetime_3(x)[1])

	df_original['STATUS'] = df_original['STATUS'].apply(lambda x: 0 if x==1 else 1)

	df_original.rename(columns={'BUS_PTNR_OID':'CID'},inplace=True)

	df_original.to_csv(DIR+'full.csv')

	# create head data(1000 rows)
	df_original.iloc[0:1000,:].to_csv(DIR+'full_head.csv')
	print('Done')



def main():
	organize_full('./original_dataset/'+DEFAULT_FULLDATA1_FILE_NAME)

if __name__ == '__main__':
	main()
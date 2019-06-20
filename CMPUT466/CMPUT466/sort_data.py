import sys, time

import pandas as pd
import numpy as np



DIR = './organized_dataset/'
SHORT_TERM = 3

seed = 7
np.random.seed(seed)

def read_sort(mode=0):
	if mode == 1:
		print('Read full data')
		df = pd.read_csv(DIR+'feature_engineered_full.csv',header=0)
	else:
		print('Read test data')
		df = pd.read_csv(DIR+'feature_engineered_test.csv',header=0)

	print('Data loading Done')

	length = 35
	length_df = df.groupby('CID').count()
	length_df.rename(columns={length_df.columns[0]:'length'}, inplace=True)
	print('Processing length:',length)

	temp = length_df[length_df['length'] == length]
	cid_list = set(temp.index.values)

	final_df = pd.DataFrame(columns=df.columns)
	count = 0
	for cid in cid_list:
		temp = df.loc[df['CID']==cid].sort_values(by='DATE')
		final_df = final_df.append(temp, ignore_index=True)

		if count % 250 == 0:
			print('%d-th CID Done'%(count))

		count += 1

	print('All(%d) CIDs Done'%(count))
	print('creating CSV')

	if mode == 1:
		final_df.iloc[:,1:].to_csv(DIR+'sorted_35_full.csv')
	else:
		final_df.iloc[:,1:].to_csv(DIR+'sorted_35_test.csv')
	print('CSV created')



def main():
	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('Start: %s\n'%(current_time_str) )

	mode = 0
	if len(sys.argv) > 1:
		if sys.argv[1] == 'full':
			mode = 1
		else:
			mode = 0

	read_sort(mode)

	current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	print('\nEnd: %s\n'%(current_time_str) )

if __name__ == '__main__':
	main()

import organize
from data_manager import DataManager

DATA_DIR = './dataset/'

def main():
	# organize original csv dataset then create new dataset files. (depicted below)
	# 
	# dataset ----- profile.csv
	# 			|
	# 			|-- transactions.csv
	# 			|
	#			|-- dependent.csv
	organize.organize()


	
	# load organized dataset and pass it to data manager
	manager = DataManager()

	manager.read_profile(DATA_DIR+'profile.csv')
	manager.read_transactions(DATA_DIR+'transactions.csv')
	manager.read_dependent(DATA_DIR+'dependent.csv')

	# feature selection (NOT IMPLEMENTED)
	manager.feature_engineering()


	# get training & test set (NOT IMPLEMENTED)
	A_train, y_train, A_test, y_test = manager.get_learning_data()





if __name__ == '__main__':
	main()
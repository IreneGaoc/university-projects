# CMPUT466

# Full data is now available(Mar. 24)

# GCP shell
Open GCP shell then type following commands.
```
mkdir /home/<YOUR_CCID>/project
cd /home/<YOUR_CCID>/project/
git clone https://github.com/yushis/CMPUT466566.git
pip3 install pandas
pip3 install numpy
pip3 install SQLAlchemy
pip3 install scikit-learn
pip3 install tensorflow

gsutil cp -r gs://projecttransaction/T9_BUS_PTNR_TRXN.csv ./original_dataset/T9_BUS_PTNR_TRXN.csv

python3 organize.py
python3 data_manager.py
python3 learn.py
```

## How to Run Learning Algorithm on Full data
Put `feature_engineered_full.csv` to `organized_dataset` directory.

Then, at `CMPUT466566` directory, run following commands.

```
python3 -u ./learn/learn_ann.py full > ./learn/learn_ann_result.out
```

Above is the case when you run `learn_ann.py` on `full` data and write outputs to `learn_ann_result.out`.

> * `full` can also be `head` for 30 customers, `test` for 2000 customers.
> * `-u` option is to print outputs incrementally.(i.e. Not print whole outputs after programs executed.)

## memo

```
gsutil cp -r gs://projecttransaction/CMPUT466566 /home/<YOUR_CCID>/project
cd /home/<YOUR_CCID>/project/CMPUT466566/
```

[Run in Background](https://janakiev.com/til/python-background/)
```
chmod +x data_manager.py
nohup python3 -u ./data_manager.py full &
cat nohup.out
ps -ef | grep data_
```

### AUC
https://stats.stackexchange.com/questions/132777/what-does-auc-stand-for-and-what-is-it

## Result
SVM didn't converge. No results.
Logistic Regression didn't converge but with results.
```
train score: 0.45764569758236406
test score: 0.4307405001623904
=== Default Prediction Accuracy ===
train: 0.7389580973952435
test: 0.7072599531615925
=== Non-Default Prediction Accuracy ===
train: 0.44705808027629196
test: 0.4208799528897115
```



## Reorganized dataset
organize.py
> 1. Changed table column name BUS_PTNR_OID -> CID
> 2. convert DDMMYYYY format of date to long
> 3. For STATUS column, on-time payment -> 0, else -> 1
> 4. create head of data only for dev. purpose

## Data manager
data_manager.py
> 1. Simple feature selection in compress_feature() method

## Dataset stats
> * total: 1266792
> * num of default: 39015
> * ratio: 0.030798268381865373
> * num of customers: 41326

For head, # of default:  6, ratio:  0.006, # of customers:  31

# belows are only applied for sample data

## Files
> dataset: organized csv files
>
> original_dataset: unorganized original csv files
>
> data_manager.py: data parser(search and get customer info)
>
> organize.py: Organize original_dataset.


## Format of Organized files
CID: customer id

 All categories are vectorized. For example, CATEGORY=GROCERIES is changed into CATEGORY_GROCERIES=1.

## Usage
### Just to Organize
> 1. put original data files into original_dataset directory.
> 2. run `python3 organize.py`

### to Retrieve transactions of specific customer
> `get_recent_transactions(self,cid,year_upto,month_upto,month_period=12)` is in `data_manager.py`

### main file
 Everything is put together in main.py
> run `python3 main.py`


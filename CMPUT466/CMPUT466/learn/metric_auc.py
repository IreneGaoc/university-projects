import tensorflow as tf
from tensorflow.keras import backend as K

# MEMO
# If you get error like ModuleNotFoundError: No module named 'tensorflow.keras',
# change line 2 to "K = tf.keras.backend"
# 

# https://www.kaggle.com/c/invasive-species-monitoring/discussion/32762
def auc(y_true, y_pred):
	auc = tf.metrics.auc(y_true, y_pred)[1]
	K.get_session().run(tf.local_variables_initializer())
	return auc
# Predicting when Mariano will be substituted in, in general

import pandas as pd
import pylab as pl
import numpy as np
import util
from sklearn import tree
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/mariano_general_sub_unified_20091011.csv")
data = data.dropna()

#dummify innings
dummy_innings,dummy_inning_names = util.pandas_dummify(data,'inning')
data = data.join(dummy_innings)
#add interaction terms
data,_ = util.pandas_add_interaction_term(data,'inning_start','inning_9')
data,_ = util.pandas_add_interaction_term(data,'inning','leverage')
data,_ = util.pandas_add_interaction_term(data,'inning_start','inning_8')


target = data.values[:,0].astype(float)
train = data.values[:,1:].astype(float)

clf = tree.DecisionTreeClassifier(max_depth=5)
actual,predictions,accuracy = util.sklearn_k_fold_predict_and_accuracy(train,target,clf,k = 10)

#assess its fit
print accuracy
print util.confusion_matrix_binary_response(actual,predictions)
# Predicting when a pitch sub will be made in general

import pandas as pd
import pylab as pl
import numpy as np
import util
from sklearn import tree
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/predict_starter_removed_team_oblivious.csv")
data = data[pd.notnull(data['pitches_since_last'])]
data = data[pd.notnull(data['position_in_lineup'])]

print data.columns.values.tolist()[3:]

target = data.values[:,2].astype(float)
train = data.values[:,3:].astype(float)

clf = tree.DecisionTreeClassifier(max_depth=5)
actual,predictions,accuracy = util.sklearn_k_fold_predict_and_accuracy(train,target,clf,k = 10)

print accuracy

#assess its fit
print util.confusion_matrix_binary_response(actual,predictions)
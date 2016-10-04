# Predicting when a pitch sub will be made in general
import pandas as pd
import pylab as pl
import numpy as np
import util
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/predict_substitution_timing_stats_team_oblivious.csv")
data = data[pd.notnull(data['pitches_since_last'])]
data = data[pd.notnull(data['position_in_lineup'])]

#convert to sklearn format
data_training = data[util.training_set_by_date_mask(data)]
data_test = data[util.test_set_by_date_mask(data)]

#grab the appropriate data and response
skl_training_data = data_training.values[:,3:].astype(float)
skl_training_response = data_training.values[:,2].astype(float)
skl_test_data = data_test.values[:,3:].astype(float)
skl_test_response = data_test.values[:,2].astype(float)

abdt = AdaBoostClassifier(tree.DecisionTreeClassifier(max_depth=5))
abdt.fit(skl_training_data,skl_training_response)

#assess its fit
predictions = abdt.predict(skl_test_data)
print util.confusion_matrix_binary_response(skl_test_response,predictions)
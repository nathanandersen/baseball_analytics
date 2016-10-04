# Predicting when Mariano will be substituted in! Only looking at 2010
import pandas as pd
import pylab as pl
import numpy as np
import util
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/mariano_given_sub_20091011.csv")


#dummify innings
dummy_innings,dummy_inning_names = util.pandas_dummify(data,'inning')
data = data.join(dummy_innings)

training_data =  data.values[:,2:].astype(float)
training_response = data.values[:,1].astype(float)

abdt = AdaBoostClassifier(tree.DecisionTreeClassifier())

abdt.fit(training_data,training_response)

#assess its fit
predictions = abdt.predict(training_data)
print util.confusion_matrix_binary_response(training_response,predictions)
util.print_missed_successes(data,training_response,predictions)
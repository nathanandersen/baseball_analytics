# Predicting when Mariano will be substituted in! Only looking at 2010

import pandas as pd
import pylab as pl
import numpy as np
import util
from sklearn import tree
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/mariano_given_sub_20091011.csv")

#dummify innings
dummy_innings,dummy_inning_names = util.pandas_dummify(data,'inning')
data = data.join(dummy_innings)

#add interaction terms
# data,_ = util.pandas_add_interaction_term(data,'inning_start','inning_9')
# data,_ = util.pandas_add_interaction_term(data,'inning','leverage')
# data,_ = util.pandas_add_interaction_term(data,'inning_start','inning_8')
features = data.columns.values.tolist()[2:]

#get training and test sets
training,test = util.pandas_training_and_test(data)
training_data =  training.values[:,2:].astype(float)
training_response = training.values[:,1].astype(float)
test_data =  test.values[:,2:].astype(float)
test_response = test.values[:,1].astype(float)

clf = tree.DecisionTreeClassifier(max_depth=5)

clf.fit(training_data,training_response)

#assess its fit
predictions = clf.predict(test_data)
print util.confusion_matrix_binary_response(test_response,predictions)
# util.print_missed_successes(data,test_response,predictions)

util.export_decision_tree_as_pdf(GLOBAL_VARS.VISUALIZATIONS_PATH + "/dtc_mariano_given_sub_20091011.dot",clf,features)
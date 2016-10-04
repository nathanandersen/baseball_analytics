# Predicting when Mariano will be substituted in, in general

import pandas as pd
import pylab as pl
import numpy as np
import util
from sklearn import tree
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/mariano_general_sub_away_20091011.csv")
data = data.dropna()

#dummify innings
dummy_innings,dummy_inning_names = util.pandas_dummify(data,'inning')
data = data.join(dummy_innings)
#add interaction terms
features = data.columns.values.tolist()[1:]

training_data =  data.values[:,1:].astype(float)
training_response = data.values[:,0].astype(float)

clf = tree.DecisionTreeClassifier()

clf.fit(training_data,training_response)

#assess its fit
predictions = clf.predict(training_data)
print util.confusion_matrix_binary_response(training_response,predictions)
#util.print_missed_successes(data,training_response,predictions)

util.export_decision_tree_as_pdf(GLOBAL_VARS.VISUALIZATIONS_PATH + "/mariano_general_sub_home_20091011.dot",clf,features)
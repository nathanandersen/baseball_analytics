# Predicting when Mariano will be substituted in! Only looking at 2010

import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import util
import GLOBAL_VARS

#set options
pd.set_option('display.max_columns', 500)

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/mariano_given_sub_20091011.csv")

#apply appropriate masks
# data = data[util.filter_middle_season(data)]

print data.head()
print data.describe()

#dummify innings
dummy_innings,dummy_inning_names = util.pandas_dummify(data,'inning')
data = data.join(dummy_innings)

#add interaction terms
interaction_names = []
data,interaction_name = util.pandas_add_interaction_term(data,'inning_start','inning_9')
interaction_names.append(interaction_name)
data,interaction_name = util.pandas_add_interaction_term(data,'inning','leverage')
interaction_names.append(interaction_name)
data,interaction_name = util.pandas_add_interaction_term(data,'inning_start','inning_8')
interaction_names.append(interaction_name)

#set the predictors
predictors = ['inning_start','leverage','outs','score_diff_lt3'] + interaction_names + dummy_inning_names
remove_from_model = ['inning_4','inning_5','inning_6','inning_7','inning_11','inning_12','inning_14','inning_10','inning_9',\
						'inning_13','inning_15','inning_3','inning_2']
predictors = [p for p in predictors if p not in remove_from_model]

print data.head()
print data.describe()

# fit the model
logit = sm.Logit(data['mariano'], data[predictors])
result = logit.fit()
print result.summary()

#assess its fit
predictions = result.predict(data[predictors])
print util.confusion_matrix_binary_response(data['mariano'].tolist(),predictions)
util.print_missed_successes(data,data['mariano'].tolist(),predictions)
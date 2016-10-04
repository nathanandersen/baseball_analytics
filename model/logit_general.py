import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import util
import GLOBAL_VARS
 
# read the data in
df = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/predict_substitution_timing_stats_team_oblivious.csv")

df_masked = df[util.training_set_by_date_mask(df)]

# df_masked_1 = df_masked[df.inning == 6]
# df_masked_2 = df_masked[df.inning > 9]
# df_masked_3 = df_masked[df.inning == 9]
# print df_masked_1.describe()
# print df_masked_2.describe()
# print df_masked_3.describe()
# df_masked = df_masked[df.leverage > 0.8]

#some pitches data seems to be MIA
df_masked = df_masked[pd.notnull(df['pitches_since_last'])]
df_masked = df_masked[pd.notnull(df['position_in_lineup'])]

#remove these?
df_masked = df_masked.drop('score_diff',1)
df_masked = df_masked.drop('top',1)
df_masked = df_masked.drop('second',1)

# take a look at the dataset
print df_masked.head()
print df_masked.describe()

#perform the logistic regression, use from fielding ownwards
train_cols = df_masked.columns[3:] 


logit = sm.Logit(df_masked['substitution'], df_masked[train_cols])
 
# fit the model
result = logit.fit()

print result.summary()

predictions = result.predict(df_masked[train_cols])
predictions = [-i for i in predictions]
exp_preds = np.exp(predictions)

print util.confusion_matrix_binary_response(df_masked['substitution'].tolist(),predictions)
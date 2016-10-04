import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import GLOBAL_VARS
 
# read the data in
df = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/substitution_when.csv")
 
def date_mask(df):
	return ((df.date > '2012-01-01') & (df.date < '2012-12-31')) |\
	((df.date > '2010-01-01') & (df.date <'2010-12-31')) |\
	((df.date > '2008-01-01') & (df.date <'2008-12-31')) |\
	((df.date > '2006-01-01') & (df.date <'2006-12-31')) |\
	((df.date > '2004-01-01') & (df.date <'2004-12-31'))


df_masked = df[date_mask(df)]
df_masked = df_masked[df.inning > 6]
df_masked = df_masked[df.leverage > 3.0]

print df_masked.head()

#some pitches data seems to be MIA
df_masked = df_masked[pd.notnull(df['pitches_since_last'])]
 
logit = sm.Logit(df_masked['substitution'], df_masked[['leverage','fielding','inning']])
 
# fit the model
result = logit.fit()

print result.summary()

predictions = result.predict(df_masked[['leverage','fielding','inning']])

small = [ i for i in predictions if i < 0.12]

big = [ i for i in predictions if i > 0.12]

print len(small)

print len(big)

print len(predictions)
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import GLOBAL_VARS

# read the data in
df = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/predict_substitution_timing_stats_team_oblivious.csv")

#df_masked_hist = df[df.inning >= 6]
df_masked_hist = df[df.substitution == 1]
#df_masked_hist = df_masked_hist[df_masked_hist.leverage > 1.5]
#df_masked_scatter = df[df.inning >= 8]

# take a look at the dataset
print df_masked_hist.head()
print df_masked_hist.describe()

#df_masked_hist['leverage'].hist(bins=50)
df_masked_hist['inning'].hist(bins=19)

#plt.scatter(df.pitches_since_last, df.substitution)

plt.show()
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import GLOBAL_VARS

# read the data in
df = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/predict_substitution_timing_stats_team_oblivious.csv")

max_leverage = df['leverage'].max()

rows_list = []
increment = max_leverage / 100

for i in np.arange(0,max_leverage,increment):
	row_dict = {}
	row_dict['leverage_average'] = i + increment / 2
	occ = df[df.leverage > i]
	occ = occ[occ.leverage < i + increment]
	if len(occ) != 0:
		print "row_created"
		print len(occ[occ.substitution == 1].index)
		row_dict['probability_of_sub'] = len(occ[occ.substitution == 1].index) / len(occ.index)
		rows_list.append(row_dict)

final_df = pd.DataFrame(rows_list)
print final_df.head()

plt.scatter(final_df.leverage_average, final_df.probability_of_sub)
plt.show()
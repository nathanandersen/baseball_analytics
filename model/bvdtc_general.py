# Predicting when a pitch sub will be made in general

import pandas as pd
import pylab as pl
import numpy as np
import util
from classification import BaseballDTCVariableEnsemble
import GLOBAL_VARS

# read the data in
data = pd.read_csv(GLOBAL_VARS.DATA_SET_PATH + "/predict_substitution_timing_stats_team_oblivious.csv")
data = data[pd.notnull(data['pitches_since_last'])]
data = data[pd.notnull(data['position_in_lineup'])]

data_training = data[util.training_set_by_date_mask(data)]
data_test = data[util.test_set_by_date_mask(data)]

#grab the appropriate response
test_data = data_test.values[:,3:].astype(float)
test_response = data_test.values[:,2].astype(float)

clf = BaseballDTCVariableEnsemble(data_training,2,3,depth=5,ntrees=20)

#assess its fit
predictions = clf.predict(test_data)
print util.confusion_matrix_binary_response(test_response,predictions)
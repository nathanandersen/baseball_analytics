# This class is an ensemble of decision tree classifiers
from sklearn import tree
import numpy as np
import util

__all__ = ["BaseballDTCEnsemble","BaseballDTCVariableEnsemble"]

class BaseballDTCEnsemble(object):

	def __init__(self,leverage_index,depth=30):
		self.ensemble_list = []
		self.leverage_index = leverage_index
		self.depth = depth

	def fit(self,training,target):
		self.ensemble_list = []
		data = np.column_stack((target,training))
		low_leverage_data = data[data[:,self.leverage_index + 1] < 1]
		med_leverage_data = data[data[:,self.leverage_index + 1] >= 1]
		med_leverage_data = med_leverage_data[med_leverage_data[:,self.leverage_index+1] < 1.7]
		high_leverage_data = data[data[:,self.leverage_index + 1] >= 1.7]
		#build decision trees
		low_leverage_clf = tree.DecisionTreeClassifier(max_depth=self.depth)
		low_leverage_clf.fit(low_leverage_data[:,1:],
								low_leverage_data[:,0])
		high_leverage_clf = tree.DecisionTreeClassifier(max_depth=self.depth)
		high_leverage_clf.fit(high_leverage_data[:,1:],
								high_leverage_data[:,0])
		med_leverage_clf = tree.DecisionTreeClassifier(max_depth=self.depth)
		med_leverage_clf.fit(med_leverage_data[:,1:],
								med_leverage_data[:,0])

		self.ensemble_list = [low_leverage_clf,med_leverage_clf,high_leverage_clf]

		return self

	@property
	def feature_importances_(self):
	    return self.ensemble_list[0].feature_importances_

	def predict(self,data):
		predictions = []
		for clf in self.ensemble_list:
			predictions.append(clf.predict(data))
		
		zipped_predictions = zip(*predictions)
		results = []
		for t in zipped_predictions:
			results.append(1 if sum(t) > 1 else 0)
		return results

	def score(self,X,Y):
		predicted = self.predict(X)
		cm = util.confusion_matrix_binary_response(Y,predicted)
		return float(cm[0][0] + cm[1][1]) / float(sum(map(sum,cm)))

class BaseballDTCVariableEnsemble(object):

	def __init__(self,pandas_data,response_index,first_predictor_index,ntrees = 3,depth=5,column='leverage'):
		self.ensemble_dict = []
		self.criterion = max(ntrees / 3 - 1,0)
		self.column = column
		self.ntrees = ntrees
		pandas_data = pandas_data.sort(self.column)
		pandas_data = pandas_data.reindex()
		step = len(pandas_data.index) / ntrees

		for i in range(self.ntrees):
			subset = pandas_data[i*step:(i+1)*step]
			clf = tree.DecisionTreeClassifier(max_depth=depth)
			clf.fit(subset.values[:,first_predictor_index:].astype(float),
					subset.values[:,response_index].astype(float))
			self.ensemble_dict[i*step,(i+1)*step] = clf

	def predict_all(self,data):
		data = data.sort(self.column)
		data = data.reindex()

		predictions = []
		for clf in self.ensemble_dict.values():
			predictions.append(clf.predict(data))

		zipped_predictions = zip(*predictions)
		results = []
		for t in zipped_predictions:
			results.append(1 if sum(t) > 2 else 0)
		return results

	def predict_some(self,data):
		predictions = {}
		
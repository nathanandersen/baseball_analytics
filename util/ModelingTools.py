# Modeling Tools !!!
# Some pretty sweet tools for all sorts of modeling fun

import pandas as pd
from pandas import DataFrame, Series
from sklearn import tree
from sklearn.externals.six import StringIO
import numpy as np
from sklearn import cross_validation

__all__ = ['pandas_add_interaction_term','confusion_matrix_binary_response','pandas_dummify',\
			'pandas_add_interaction_with_list_of_variables','print_missed_successes',
			'export_decision_tree_as_pdf','pandas_training_and_test','sklearn_k_fold_predict_and_accuracy']

def pandas_add_interaction_term(df,col_1_name,col_2_name):
	df_local = df.copy()
	interaction_name = col_1_name +"*"+col_2_name
	df_local[interaction_name] = df_local[col_1_name] * df_local[col_2_name]
	return df_local,interaction_name

def pandas_add_multi_interaction_term(df,list_names):
	pass

def pandas_dummify(df,variable_name):
	dummy_variables = pd.get_dummies(df[variable_name], prefix=variable_name)
	dummy_variables_names = dummy_variables.columns.values.tolist()
	dummy_variables_to_keep = dummy_variables_names[1:]
	return dummy_variables,dummy_variables_to_keep

def pandas_add_interaction_with_list_of_variables(df,variable_name,variable_list):
	interaction_names = []
	for name in variable_list:
		df,iname = pandas_add_interaction_term(df,variable_name,name)
		interaction_names.append(iname)
	return df,interaction_names

#takes as input two lists and returns nested lists. Actual is on column, predicted on row
def confusion_matrix_binary_response(actual_response,predicted_response):
	#inner lists are the rows
	confusion_matrix = [[0,0],[0,0]]
	for a,p in zip(actual_response,predicted_response):
		a = int(a)
		#just really need to round p
		p = 1 if p> 0.5 else 0
		confusion_matrix[a][p] += 1
	return confusion_matrix

def print_missed_successes(df,actual_response,predicted_response):
	for i,(a,p) in enumerate(zip(actual_response,predicted_response)):
		a = int(a)
		p_prime = 1 if p> 0.5 else 0
		if a != p_prime and a == 1:
			print "MISS -----------"
			print p
			print df.iloc[[i]]

def export_decision_tree_as_pdf(filename,decision_tree,features):
	with open(filename, 'w') as f:
		f = tree.export_graphviz(decision_tree, out_file=f,feature_names=features)

#splits data frame into test and training, approximately the same size
def pandas_training_and_test(data_frame):
	np.random.seed(69) #LOL
	test_sample_size = len(data_frame.index) / 2
	training_sample_size = len(data_frame.index) - test_sample_size
	test_rows = np.random.choice(data_frame.index, size=test_sample_size, replace=False)
	training_data = data_frame.copy(deep=True)
	training_data.drop(data_frame.index[test_rows])
	return training_data,data_frame.ix[test_rows]

def sklearn_k_fold_predict_and_accuracy(train,target,clf,k = 10):
	cv = cross_validation.KFold(len(train),k=k,indices = False)
	results = []
	actual = []
	accuracy = 0

	for traincv,testcv in cv:
		pred = clf.fit(train[traincv],target[traincv]).predict(train[testcv])
		actual.extend(target[testcv])
		results.extend(pred)
		accuracy = accuracy + clf.score(train[testcv],target[testcv])
		print len(results)
		print accuracy
		print clf.feature_importances_

	return actual,results,accuracy / k

def bdc_k_fold_predict_and_accuracy(data,clf,k = 10):
	cv = cross_validation.KFold(len(data),k=k,indices = False)
	results = []
	actual = []
	accuracy = 0

	for traincv,testcv in cv:
		train_data = data[traincv]
		test_data = data[testcv]
		pred = clf.fit(train[traincv],target[traincv]).predict(train[testcv])
		actual.extend(target[testcv])
		results.extend(pred)
		accuracy = accuracy + clf.score(train[testcv],target[testcv])
		print len(results)
		print accuracy	

	return actual,results,accuracy / k
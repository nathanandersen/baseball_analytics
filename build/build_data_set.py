# Builds one of the basic data sets - the one to predict when 
# pitching substitutions occur
from game_model import BaseballDomain

import cPickle as pickle
import os
import argparse
import csv
import saber.data_sets
from GLOBAL_VARS import *

#create the argument parser
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("function_name",type=str)
argument_parser.add_argument("file_name",type=str)
argument_parser.add_argument("--years",nargs='+',type=int)

def add_stats_from_domains(dir_list,saber_function,data):
	for year in dir_list:
		domain = BaseballDomain.from_files(PARSED_DATA_PATH + "/" + year + "/" + GAME_FILE_NAME + ".pkl",
											PARSED_DATA_PATH + "/" + year + "/" + ROSTER_FILE_NAME,
											PARSED_DATA_PATH + "/" + FREQ_FILE_NAME + ".pkl")
		for row in saber_function(domain):
			data.append(row)

def write_data_set(data,header_function,FILENAME):
	with open(DATA_SET_PATH + "/" + FILENAME,'wb') as csvfile:
	    csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

	    #ask function to give the headers
	    csvwriter.writerow(header_function())

	    for row in data:
	        csvwriter.writerow(row)

if __name__ == "__main__":
	args = argument_parser.parse_args()
	dir_list = None
	if args.years:
		dir_list = [str(y) for y in args.years]
	else:
		dir_list = [ name for name in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, name)) ]

	data = []
	saber_function = getattr(saber.data_sets,args.function_name)
	header_function = getattr(saber.data_sets,args.function_name+'_headers')
	add_stats_from_domains(dir_list,saber_function,data)
	write_data_set(data,header_function,args.file_name)
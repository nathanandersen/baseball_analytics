# This script will parse all the data in data_raw from games

import cPickle as pickle
from parser import *
import os
import argparse
from GLOBAL_VARS import *

#create the argument parser
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--years",nargs='+',type=int)

def parse_games(dir_list):
	for year in dir_list:
		data = []
		for data_file in os.listdir(RAW_DATA_PATH + "/" + year):
			_,extension = os.path.splitext(data_file)
			if extension.startswith(".EV"):
				american_league = True if extension == ".EVA" else False
				game_parser = RetrosheetParser(RAW_DATA_PATH + "/" + year + "/" + data_file,american_league,DEBUG)
				for g in game_parser.games():
					data.append(g)

		#write list to file
		game_list_file = open(PARSED_DATA_PATH + "/" + year + "/" + GAME_FILE_NAME + ".pkl", 'wb')
		pickle.dump(data, game_list_file)
		game_list_file.close()

if __name__ == "__main__":
	args = argument_parser.parse_args()
	dir_list = None
	if args.years:
		dir_list = [str(y) for y in args.years]
	else:
		dir_list = [ name for name in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, name)) ]

	parse_games(dir_list)
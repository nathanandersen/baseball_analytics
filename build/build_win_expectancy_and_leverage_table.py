# This script will take a pickle file with a list of games
# as a commandline argument and will build a win expectancy
# table. by default through the ninth inning, though maybe later

import cPickle as pickle
import os
import argparse
from saber import *
from GLOBAL_VARS import *

#create the argument parser
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--years",nargs='+',type=int)

if __name__ == "__main__":
    args = argument_parser.parse_args()
    dir_list = None

    if args.years:
        dir_list = [str(y) for y in args.years]
    else:
        dir_list = [ name for name in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, name)) ]

    freq_tracker_table = GameStateFrequencyTrackerTable()

    for year in dir_list:
        #load game list
        game_list_file = open(PARSED_DATA_PATH + "/" + year + "/" + GAME_FILE_NAME + ".pkl", 'rb')
        game_list = pickle.load(game_list_file)
        game_list_file.close()
        freq_tracker_table.add_data_from_game_list(game_list)

    #now convert to a lighter weight representation
    freq_table = freq_tracker_table.as_game_state_frequency_table()

    #build win exp table and write to file
    game_frequency_table_file = open(PARSED_DATA_PATH + "/" + FREQ_FILE_NAME + ".pkl", 'wb')
    pickle.dump(freq_table, game_frequency_table_file)
    game_frequency_table_file.close()

from parser import *
from game_model import *
import cPickle as pickle

game_list_file = open("data_parsed/2010/game_list.pkl", 'rb')
game_list = pickle.load(game_list_file)
game_list_file.close()

for g in game_list:
	print repr(g)
	break
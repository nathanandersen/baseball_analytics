# This script will parse all the data in data_raw from games
# played in the american league.

from parser import *
import os

count = 0
for data_file in os.listdir("data_raw/2010"):
	_,extension = os.path.splitext(data_file)
	if extension == ".EVN" or extension == ".EVA":
		game_parser = RetrosheetParser("data_raw/2010/" + data_file,True,debug=True)
		for g in game_parser.games():
			#print str(g)
			count = count + 1

print count

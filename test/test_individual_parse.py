# This script will parse all the data in data_raw from games
# played in the american league.

from parser import *

count = 0

game_parser = RetrosheetParser("data_raw/2012/2012PHI.EVN",True,debug=True)
for g in game_parser.games():
	count = count + 1
	#print str(g)
	break

print count

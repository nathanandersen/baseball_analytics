# This script will parse all the data in data_raw from games
# played in the american league.

from parser import *

game_parser = RetrosheetParser("data_raw/2012/2012ANA.EVA",True,debug=True)
for g in game_parser.games():
	for s in g.pitching_substitutions:
		print s
	break

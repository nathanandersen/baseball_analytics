from parser import *

count = 0
game_parser = RetrosheetParser("data_raw/2012/2012ANA.EVA",True,debug=True)
for g in game_parser.games():
	print repr(g.pitchers)
	count += 1

	if count == 4:
		break
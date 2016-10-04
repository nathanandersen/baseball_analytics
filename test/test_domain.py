from game_model import BaseballDomain

domain = BaseballDomain.from_files("data_parsed/2012/game_list.pkl","data_parsed/2012/all_players.csv","data_parsed/frequency_table.pkl")
for pitcher in domain.pitchers:
	print domain.pitchers[pitcher]

print len(domain.pitchers)
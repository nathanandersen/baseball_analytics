# DOMAIN - 
# The domain is the context in which these baseball games occur. This 
# could be as broad as multiple seasons, all teams. Or it could be as narrow
# as one season, one team.
import game_model
import csv
import cPickle as pickle

__all__ = ['BaseballDomain']

class BaseballDomain(object):
	def __init__(self):
		self.games = []
		self.pitchers = {}
		self.teams = {}
		self.win_exp_table = None

	#initialize from files
	@classmethod
	def from_files(cls,game_list_file,player_list_file,win_exp_table_file):
		domain = BaseballDomain()
		
		#initially we add all players, but we flag based on whether or not they are pos players
		with open(player_list_file,'rb') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',',quotechar='"')
			for row in csvreader:
				domain.pitchers[row[0]] = game_model.Pitcher(row[0],row[1],row[2],row[4])
		with open(game_list_file,'rb') as game_list_file:
				domain.games = pickle.load(game_list_file)
		with open(win_exp_table_file,'rb') as win_exp_table_file:
				domain.win_exp_table = pickle.load(win_exp_table_file)

		domain._build_team_dict()
		domain._build_pitcher_associations()
		domain._clean_pitcher_list()
		return domain

	def _build_team_dict(self):
		for game in self.games:
			if game.home_team not in self.teams:
				self.teams[game.home_team] = game_model.Team(game.home_team)
			if game.away_team not in self.teams:
				self.teams[game.away_team] = game_model.Team(game.away_team)
			self.teams[game.home_team].games.append(game)
			self.teams[game.away_team].games.append(game)

	def _build_pitcher_associations(self):
		for game in self.games:
			for pitcher in game.pitchers:
				self.pitchers[pitcher].add_appearance(game.pitchers[pitcher])

	def _clean_pitcher_list(self):
		d_copy = dict(self.pitchers)
		for pitcher in self.pitchers:
			if self.pitchers[pitcher].appearances.empty and self.pitchers[pitcher].position_player:
				del d_copy[pitcher]

		self.pitchers = d_copy
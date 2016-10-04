# GAME -
# class for modelling baseball games. Tracks all data it can based on single game
# additional passes through the games done later

import util

__all__=["Game"]

class Game(object):
	def __init__(self,
					game_date,
					home_team,
					away_team,
					home_roster,
					away_roster,
					american_league,
					game_progression,
					pitchers,
					pitching_substitutions):
		#string
		self.home_team = home_team
		# string
		self.away_team = away_team
		#datetime object
		self.date = game_date
		# list of pitching sub objects
		self.pitching_substitutions = pitching_substitutions
		#list of game states
		self.game_progression = game_progression
		# true or false - whether game is played by NL or AL rules
		self.american_league = american_league
		#should be a pitcher dict
		self.pitchers = pitchers

		#GameRoster Objects
		self.home_roster = home_roster
		self.away_roster = away_roster

	def __str__(self):
		return "Game: "+str(self.date) +" | "+self.home_team+" vs. "+self.away_team+" | "+str(self.score_home)+" - "+str(self.score_away)

	def __repr__(self) :
		rep = self.__str__()
		rep = rep + "\n\t GAMESTATES - "
		for state in self.game_progression :
			rep = rep +"\n\t\t"+str(state)
		rep = rep + "\n\t PITCHING SUBSTITUTIONS - "
		for sub in self.pitching_substitutions :
			rep = rep +"\n\t\t"+str(sub)
		rep = rep + "\n\t HOME ROSTER - \n"
		rep = rep + util.reindent(repr(self.home_roster),2)
		rep = rep + "\n\t AWAY ROSTER - \n"
		rep = rep + util.reindent(repr(self.away_roster),2)
		return rep

	@property
	def score_home(self):
		return self.game_progression[-1].score_home	
	@property
	def score_away(self):
		return self.game_progression[-1].score_away

	#returns who won
	def win(self,home=True):
		if home:
			return self.score_home - self.score_away > 0
		return self.score_home - self.score_away < 0
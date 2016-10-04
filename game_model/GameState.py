# GAMESTATE - 
# Classes for the internal represenation of the game state
__all__=["GameState"]

import error
import game_model
import util

#innings are actually double the actual inning to allow for top and bottom
#immutable game state - not enforced but should be treated as such
class GameStateBase(object):
	def __init__(self,score_home,score_away,inning,outs,base_runners):
		#check to make sure certain bounds are met
		self.inning = inning
		self.base_runners = base_runners
		self.outs = outs
		self.score_home = score_home
		self.score_away = score_away

		#tagged later - used to build data set later
		self.pitching_appearance_tracker_home = None
		self.pitching_appearance_tracker_away = None
		self.change_in_leverage = None
		self.position_in_lineup_home = None
		self.position_in_lineup_away = None
		self.batter_id = None

	def __hash__(self):
		return NotImplemented

class GameState(GameStateBase):
	def __init__(self,score_home,score_away,inning,outs,base_runners):
		GameStateBase.__init__(self,score_home,score_away,inning,outs,base_runners)

		#this attribute is tagged to it later on, mainly used to debug
		#not considered in terms of checking equality
		self.transition_code = None

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "<GameState: Home - {0} | Away - {1} | {2} | {3} outs | {4} | {5} | {6} >".format(self.score_home,\
																						self.score_away,\
																						self.inning,\
																						self.outs,\
																						self.base_runners,\
																						self.transition_code,
																						self.batter_id)
	#checks for equality between two game states, ignoring trans codes
	#in reality it actually checks to see if they are in the same EQUIVALENCE CLASS
	def __eq__(self,other):
		return isinstance(other,self.__class__)\
				and other.inning == self.inning\
				and other.base_runners == self.base_runners\
				and other.outs == self.outs\
				and other.score_home - other.score_away == self.score_home - self.score_away

	def __ne__(self,other):
		return not (self == other)

	#interpreted as follows : IIBBBSDDO
	#hash is based on equivalence class of game states
	def __hash__(self):
		h = 1
		#give two places to inning
		ir = self.inning.inning_rep
		h = 10*h + ir if ir >= 10 else 100*h + ir
		#give three places to br
		h = 10*h + 1 if self.base_runners.first else 10*h
		h = 10*h + 1 if self.base_runners.second else 10*h
		h = 10*h + 1 if self.base_runners.third else 10*h
		#three places for score differential
		sd = self.score_home - self.score_away
		h = 10*h if sd >= 0 else 10*h + 1
		h = 10*h + abs(sd) if abs(sd) >= 10 else 100*h + abs(sd)
		#add outs
		h = 10*h + self.outs

		return h

	#list repr of game state, contains info up to equivalence
	def to_list(self,perspective_home = True):
		half = "bottom" if self.inning.bottom else "top"
		sd = self.score_home - self.score_away if perspective_home else self.score_away - self.score_home
		f = "1st" if self.base_runners.first else "X"
		s = "2nd" if self.base_runners.second else "X"
		t = "3rd" if self.base_runners.third else "X"
		return [self.inning.number,half,sd,self.outs,f,s,t]

	def to_numeric_list(self,perspective_home = True):
		half = 0 if self.inning.top else 1
		sd = self.score_home - self.score_away if perspective_home else self.score_away - self.score_home
		f = 1 if self.base_runners.first else 0
		s = 1 if self.base_runners.second else 0
		t = 1 if self.base_runners.third else 0
		return [self.inning.number,half,sd,self.outs,f,s,t]

	def compress_state(self):
		if self.inning.number > 9:
			return GameState(self.score_home,self.score_away,Inning(9,self.inning.bottom),self.outs,self.base_runners)
		return self

	def position_in_lineup(self,perspective_home):
		return self.position_in_lineup_away if perspective_home else self.position_in_lineup_home

	def score_differential(self,perspective_home = True):
		return self.score_home - self.score_away if perspective_home else self.score_away - self.score_home

	#returns the start game state - 0-0, Top 1, Nobody On, No Outs
	@classmethod
	def start(cls):
		return GameState(0,0,game_model.Inning.start(),0,game_model.BaseRunners(False,False,False))

	#returns innings elapsed from perspective of home or away team for pitch sub purposes
	#it is assumed user passes start_state first, then end state. And that end >= start
	#this method needs to be cleaned up
	@classmethod
	def innings_pitched(cls,start_state,end_state,home=True):
		innings = 0
		partial_innings = 0
		if start_state.inning.top and home == True:
			# means pitching sub in happens during pitching
			if start_state.inning.number < end_state.inning.number:
				if start_state.outs != 0:
					partial_innings += (3 - start_state.outs)
				else:
					innings += 1
				innings += (end_state.inning.number - start_state.inning.number - 1)
				if end_state.inning.top:
					partial_innings += end_state.outs
			elif end_state.inning.bottom:
				innings += 1
			else:
				partial_innings += end_state.outs - start_state.outs

		elif start_state.inning.top and home == False:
			if start_state.inning.number < end_state.inning.number:
				innings += end_state.inning.number - start_state.inning.number
			if end_state.inning.bottom:
				partial_innings += end_state.outs

		#so we are in the bottom of an inning at start_state
		elif home == True:
			if start_state.inning.number < end_state.inning.number:
				innings += end_state.inning.number - start_state.inning.number
			if end_state.inning.top:
				partial_innings += end_state.outs			
		elif home == False:
			if start_state.inning.number < end_state.inning.number:
				if start_state.outs != 0:
					partial_innings = 3 - start_state.outs
				else:
					innings += 1
				innings += end_state.inning.number - start_state.inning.number - 1
				if end_state.inning.bottom:
					partial_innings += end_state.outs
			elif end_state.inning.top:
				innings += 1
			else:
				partial_innings += end_state.outs - start_state.outs

		return util.InningNumber(innings,partial_innings)

	#transition function given a retrosheet play code
	def transition_retrosheet(self,code):
		updated_score_away  = self.score_away
		updated_score_home = self.score_home

		#first parse base runner movements	
		play_info = code.split(",")

		#works because in Python 0 == False
		inning = game_model.Inning(int(play_info[1]),int(play_info[2]))

		#update runners position, only want to pass the play code itself
		runs_scored,outs_incurred,updated_base_runners = self.base_runners.advance_runners_retrosheet(code.split(",")[6])
		updated_outs = self.outs + outs_incurred

		#figure out which score to increment
		if self.inning.top:
			updated_score_away += runs_scored
		else:
			updated_score_home += runs_scored

		#now, if there are fewer than 3 outs, don't transition innings
		if updated_outs < 3:
			return GameState(updated_score_home,\
							updated_score_away,\
							inning,updated_outs,\
							updated_base_runners)
		if updated_outs == 3:
			return GameState(updated_score_home,\
							updated_score_away,\
							inning.next(),\
							0,\
							game_model.BaseRunners(False,False,False))

		#should never be MORE than three outs
		raise error.InvalidGameState("There are "\
										+ str(updated_outs)\
										+" incurred in this inning, an impossibility")
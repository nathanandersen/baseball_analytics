# PITCHER - 
# Model for individual pitchers. This will be verry useful in computing
# how tired each pitcher is at the date of substitution - we can just ask the pitcher!

from datetime import date as Date
import util
import copy
import game_model

__all__ = ["Pitcher","PitchingAppearance","PitchingAppearanceDictionary","PitchingAppearanceTracker"]

class Pitcher(object):

	def __init__(self,ident,name,handedness,position):
		self.appearances = util.BinarySearchTree(util.date_key)
		self.id = ident
		self.name = name
		self.handedness = handedness
		self.pitcher = position == 'P'

	# place holder for whatever statistic of restedness is eventually used
	def rest_statistic(self,date):
		return NotImplemented

	def closer_ranking(self,date):
		return NotImplemented

	@property
	def position_player(self):
	    return not self.pitcher

	#maintains a sorted list of pitching appearances
	def add_appearance(self,appearance):
		self.appearances.insert(appearance)

	def __str__(self):
		return "<{0} | {1} | {2}>".format(self.id,self.name,self.handedness)

	def __repr__(self):
		rep = "<{0} | {1} | {2}".format(self.id,self.name,self.handedness)
		for pa in self.appearances:
			rep = rep + "\n" + str(pa)

		return rep + "\n>"
# models a pitching appearance
class PitchingAppearance(object):

	def __init__(self,date,start_state,end_state,innings_pitched,pitches_thrown,walks,hits):
		self.date = date
		self.pitches_thrown = pitches_thrown
		self.innings_pitched = innings_pitched
		self.walks = walks
		self.hits = hits

	#want to sort by date, smaller date means earlier appearance
	def __cmp__(self,other):
		if self.date == other.date:
			return 0
		return -1 if self.date < other.date else 1

	def __str__(self):
		return "<{0} | {1} IP | {2} PT | {3} WH >".format(self.date,self.innings_pitched,self.pitches_thrown,self.walks + self.hits)

#wraps a dict for repr and str purposes
class PitchingAppearanceDictionary(dict):

	def __str__(self):
		s = "Pitching Appearances by :"
		for p in self.keys():
			s = s + "\n\t" + p
		return s

	def __repr__(self):
		s = "Pitching Appearances by :"
		for p in self.keys():
			s = s + "\n\t" + p + " - " + str(self[p])
		return s

#tracks pitching appearances
class PitchingAppearanceTracker(object):

	def __init__(self,date,start_state,pitcher):
		self.pitches = 0
		self.hits = 0
		self.walks = 0
		self.start_state = start_state
		self.pitcher = pitcher
		self.date = date

	#takes the end_state and whether this pitcher is for the home or away team
	def to_pitching_appearance(self,end_state,home_team):
		return game_model.PitchingAppearance(self.date,
												self.start_state,
												end_state,
												game_model.GameState.innings_pitched(self.start_state,end_state,home_team),
												self.pitches,
												self.walks,
												self.hits)

	def deepcopy(self):
		dc = PitchingAppearanceTracker(self.date,self.start_state,self.pitcher)
		dc.pitches = self.pitches
		dc.hits = self.hits
		dc.walks = self.walks
		return dc
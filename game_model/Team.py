# TEAM - 
# A class to model a baseball team

__all__ = ["Team"]

class Team(object):
	def __init__(self,name):
		self.name = name
		self.games = []

	#want to also track Rosters over time - maybe this will be useful
	def add(self):
		pass
# GAME ROSTER - MODELS THE ROSTERS FOR EACH GAME
# lineup is a mapping between players and their batting order number
# batting order position of zero means that the player is not batting

from error import RosterError

__all__ = ["GameRoster"]

class GameRoster(object):

	def __init__(self):
		#need to set up lineup
		self.lineup = []
		for i in range(10):
			self.lineup.append(None)
		self.roster = []
		self._last_batter_position = 0

	def add(self,order,player):
		self.roster.append(player)
		#just want to maske sure it is actually an integer
		self.lineup[int(order)] = player.strip()

	# asympototically constant time
	def position(self,player):
		for i,b in enumerate(self.lineup):
			if player.strip() == b:
				return i
		raise RosterError("Roster Error - Couldn't find " + player)

	#the current position is actually one PAST the last batter
	def current_position(self):
		return (self._last_batter_position + 1) % 9

	def last_batter(self,last_batter):
		self._last_batter_position = self.position(last_batter)		

	@property
	def full(self):
	    full = True
	    for b in self.lineup[1:]:
	    	if b is None:
	    		full = False
	    return full

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		rep = "FINAL LINEUP - "
		for b in self.lineup:
			rep = rep + "\n\t " + str(b)
		rep = rep + "\nGAME ROSTER - "
		for b in self.roster:
			rep = rep + "\n\t " + str(b)
		return rep
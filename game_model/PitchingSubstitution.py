# PITCHING SUBSTITUTION - 
# Class to model pitching substitutions.
# for example would contain a reference to a gamestate
# number of pitches since last pitching substitution.
# more attributes may be added later

__all__ = ["PitchingSubstitution"]

class PitchingSubstitution(object):

	def __init__(self,pitcher_id,team_id,home_team,gamestate,pitches_since_last_substitution,position_in_lineup):
		#want to make sure to cull extra white-space - could be an issue
		self.pitcher_id = pitcher_id.strip()
		self.team_id = team_id.strip()
		self.home_team = home_team
		self.gamestate = gamestate
		self.pitches_since_last_substitution = pitches_since_last_substitution
		self.position_in_lineup = position_in_lineup

		self.batter_handedness = None
		self.pitcher_handedness = None

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "<Pitching Substitution: {0} | {1} | {2} | {3} | {4} >".format(self.pitcher_id,
																					self.pitches_since_last_substitution,
																					self.gamestate,
																					"HOME" if self.home_team else "AWAY",
																					self.position_in_lineup)
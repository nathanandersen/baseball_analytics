# BASE RUNNERS - 
# Want to subclass tuples, its immutable and lightweight
# constructor should take three booleans, representing bases occupied
# this contains logic to, given a retrosheet code (or not implemented, 
# but could ultimately be, any data source), compute the motion of the base runners
# and update a RunnerMotion object passed in
__all__=["BaseRunners"]

import game_model
import re
import error

#useful mappings and regular expressions, want to just gen once
BASE_TO_INT = {"B" : 0,"1" : 1,"2" : 2,"3" : 3,"H" : 4}
INT_TO_BASE = {0 : "B",1 : "1",2 : "2",3 : "3",4 : "H"}
PRIMARY_PLAY_OUTS = re.compile('\(\w\)')
FIELDED = re.compile('\d')
PRIMARY_PLAY_OUTS = re.compile('\(\w\)')
SECONDARY_PLAY_ERROR = re.compile('\(\d*E\d*\)')

#NOTE - this does not need magic comparator methods because it inherits from tuple
class BaseRunners(tuple):

	def __new__(cls, first, second,third):
		return tuple.__new__(cls, (first, second, third))

	@property
	def first(self):
		return tuple.__getitem__(self, 0)

	@property
	def second(self):
		return tuple.__getitem__(self, 1)

	@property
	def third(self):
		return tuple.__getitem__(self, 2)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if self.first:
			if self.second:
				if self.third:
					return "<BaseRunners: Base runners on first, second and third>"
				else:
					return "<BaseRunners: Base runners on first and second>"
			elif self.third:
				return "<BaseRunners: Base runners on first and third>"
			else:
				return "<BaseRunners: Base runner on first>"
		elif self.second:
			if self.third:
				return "<BaseRunners: Base runners on second and third>"
			else:
				return "<BaseRunners: Base runner on second>"
		elif self.third:
			return "<BaseRunners: Base runner on third>"
		else:
			return "<BaseRunners: No Base runners>"
	
	def __setattr__(self, *ignored):
		return NotImplemented
	def __delattr__(self, *ignored):
		return NotImplemented
	def __getitem__(self, item):
		raise TypeError

	@classmethod
	def bases_empty(cls):
		return BaseRunners(False,False,False)

	#returns new base_runner positions, runs scored and outs
	def advance_runners_retrosheet(self,play_code):
		#captures runner motion
		runner_motion = game_model.RunnerMotion(self)
		self._process_primary_play_retrosheet(play_code,runner_motion)
		self._process_secondary_play_retrosheet(play_code,runner_motion)

		return runner_motion.get_result_of_motion()

	#in the retrosheet scoring system this encompasses the event itself plus outs made on the primary play
	def _process_primary_play_retrosheet(self,full_play_code,runner_motion):
		#want to ignore secondary portions, but may be more than one primary play
		primary_play_code = full_play_code.split(".")[0]
		ground_double_play = "GDP" in primary_play_code
		ground_triple_play = "GTP" in primary_play_code
		air_double_play = "LDP" in primary_play_code or "FDP" in primary_play_code
		air_triple_play = "LTP" in primary_play_code or "FTP" in primary_play_code
		other_double_play = "DP" in primary_play_code and not (air_triple_play or air_double_play)

		#we want to get rid of everrything after the / now bc only info we wanted was DP info
		#codes might contain multiple plays denoted by other semicolons or +
		primary_play_codes_0 = full_play_code.split(".")[0].split("/")[0].split("+")
		primary_play_codes = []
		for code in primary_play_codes_0:
			primary_play_codes = primary_play_codes + code.split(";")

		#play code iterator, filters out empty codes
		play_code_it = (p for p in primary_play_codes if p != "" )
		for play_code in play_code_it:
			#many different cases for what can occur on the play
			if play_code.startswith("SB"):
				start_base = BASE_TO_INT[play_code[2]] - 1
				self._check_runner_at_start_base(runner_motion,start_base)
				runner_motion[start_base] = start_base + 1
			elif play_code.startswith("CS"):
				start_base = BASE_TO_INT[play_code[2]] - 1
				self._check_runner_at_start_base(runner_motion,start_base)
				runner_motion[start_base] = -1
			elif play_code.startswith("POCS"):
				start_base = BASE_TO_INT[play_code[4]] - 1
				self._check_runner_at_start_base(runner_motion,start_base)
				runner_motion[start_base] = -1
			elif play_code.startswith("PO"):
				start_base = BASE_TO_INT[play_code[2]]
				self._check_runner_at_start_base(runner_motion,start_base)
				runner_motion[start_base] = -1
			#WP = Wild Pitch
			elif play_code.startswith("WP"):
				pass
			#Balk
			elif play_code.startswith("BK"):
				pass
			elif play_code.startswith("PB"):
				pass
			elif play_code.startswith("S"):
				runner_motion[0] = 1
			elif "E" in play_code:
				runner_motion[0] = 1
			#Hit by pitch and walks
			elif play_code.startswith("HP"):
				runner_motion[0] = 1
			elif play_code.startswith("W"):
				runner_motion[0] = 1
			elif play_code.startswith("IW"):
				runner_motion[0] = 1
			#ground rule double
			elif play_code.startswith("DGR"):
				runner_motion[0] = 2
			#wtf is DI??
			elif play_code.startswith("DI"):
				pass
			elif play_code.startswith("D"):
				runner_motion[0] = 2
			elif play_code.startswith("T"):
				runner_motion[0] = 3
			elif play_code.startswith("HR"):
				runner_motion[0] = 4				
			#batter is out on primary play
			elif play_code.startswith("K"):
				runner_motion[0] = -1
			#this means no play, usually a substitution is made
			elif play_code.startswith("NP"):
				pass
			#Foul ball error
			elif play_code.startswith("FLE"):
				pass
			#"Other Advance" - could be if the catcher fumbles the ball, say
			elif play_code.startswith("OA"):
				pass
			#on the fielders choice only need to encode what happens to the batter
			#here, the rest is contained in runner movements
			elif play_code.startswith("FC"):
				runner_motion[0] = 1

			#Lastly, some balls are fielded and a hit is not awarded, need to determine who is put out
			elif FIELDED.match(play_code) :
				#sometimes batter being out is not coded...
				runners_out_on_play = PRIMARY_PLAY_OUTS.findall(play_code)
				for runner in runners_out_on_play:
					runner_motion[BASE_TO_INT[runner[1]]] = -1

				#this is not technically correct, but should have same effect
				#also not sure how to tell, no way to really know what base you are at...
				if ground_double_play or other_double_play:
					#either only one runner is marked as out OR two are, but one is the batter
					#sometimes one or none are actually marked on the primary play!
					if len(runners_out_on_play) <= 1:
						runner_motion[0] = -1
					elif "(B)" not in runners_out_on_play:
						runner_motion[0] = 1
				elif ground_triple_play:
					if len(runners_out_on_play) == 2:
						runner_motion[0] = -1
					elif "(B)" not in runners_out_on_play:
						runner_motion[0] = 1
				elif air_triple_play or air_double_play :
					runner_motion[0] = -1
				#not a double or triple play, just a single out - but it might not be runner to first
				elif len(runners_out_on_play) == 1:
					runner_motion[0] = 1
				else:
					runner_motion[0] = -1

			#this means ball was fielded by catcher and he made an error
			elif play_code.startswith("C"):
				runner_motion[0] = 1

			#if we encounter a code we do not know how to handle, raise a parse error
			else:
				raise error.ParseError("Encountered Unknown Play Code "+full_play_code)

	#captures both movement made after the primary play (such as extra bases taken by the batter) or
	#can also capture movement made by other runners or outs on the bases after the primary play
	def _process_secondary_play_retrosheet(self,play_code,runner_motion):
		#a secondary play may not even occur
		if not "." in play_code:
			return runner_motion

		secondary_movements = play_code.split(".")[1].split(";")

		for movement in secondary_movements:
			if "-" in movement:
				locations = movement.split("-")
				start_base = BASE_TO_INT[locations[0][0]]
				self._check_runner_at_start_base(runner_motion,start_base)
				runner_motion[start_base] = BASE_TO_INT[locations[1][0]]

			elif "X" in movement:
				locations = movement.split("X")
				start_base = BASE_TO_INT[locations[0][0]]
				end_base = BASE_TO_INT[locations[1][0]]
				self._check_runner_at_start_base(runner_motion,start_base)

				#But now there is a second concern. There may have been an error on the play
				#in which case it would be recorded like this, but the error would be marked
				if SECONDARY_PLAY_ERROR.search(locations[1]):
					runner_motion[start_base] = end_base
				else:
					runner_motion[start_base] = -1

	def _check_runner_at_start_base(self,runner_motion,base):
		try:
			runner_motion[base]
		except KeyError:
			raise error.InvalidGameState("Cannot have runner move from base " + INT_TO_BASE[base] \
												+ " because no runner started there")

	@classmethod
	def enumerate_combinations(cls):
		for i in range(2**3):
			first,second,third = False,False,False
			if i & 1:
				first = True
			if i & 2:
				second = True
			if i & 4:
				third = True

			yield BaseRunners(first,second,third)
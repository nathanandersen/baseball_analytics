# RETROSHEET PARSER - 
# parses game data found in retrosheet files
# has a method called games which yields an iterator
# over the games in the input file that it can parse correctly

import game_model
from game_model import PitchingAppearanceTracker
from datetime import datetime as GameTime
import sys
import error
import re

__all__ = ["RetrosheetParser"]


#Regular Expressions for Processing Pitch Codes
PITCHER_PICKOFF = re.compile("\d")
CATCHER_PICKOFF = re.compile("\+\d")
UNKNOWN_PITCH_CODE = re.compile("\.|\*|\>")

class RetrosheetParser(object) : 
	def __init__(self,filename,american_league,debug=False):
		#want to open the file and store the list of its 
		with open(filename) as fp :
			self.data = list(fp)
		self.iter_index = 0
		self.filename = filename
		self.debug = debug
		self.american_league = american_league

	def games(self):
		while self.iter_index < len(self.data):
			skip_game = False
			skip_game,home_team,away_team,start_home,start_away,home_roster,away_roster,date = self._get_game_info()
			next = self.data[self.iter_index].strip()
			self.iter_index += 1

			#initialize data
			current_state = game_model.GameState.start()
			current_batter = None
			current_pitches = None
			game_states = []
			pitching_substitutions = {}
			pitcher_appearance_home = PitchingAppearanceTracker(date,current_state,start_home)
			pitcher_appearance_away = PitchingAppearanceTracker(date,current_state,start_away)
			pitchers = game_model.PitchingAppearanceDictionary()
			current_state.pitching_appearance_tracker_home = pitcher_appearance_home.deepcopy()
			current_state.pitching_appearance_tracker_away = pitcher_appearance_away.deepcopy()

			#iterate and make game states until we hit the next identifier
			while not next.startswith("id") and self.iter_index < len(self.data) and not skip_game:
				if next.startswith("play") :
					next_state,next_pitches,next_batter,skip_game = self._try_to_parse_next(game_states,current_state,next)
					#if error occured, skip this game
					if skip_game:
						break
					#make sure state transitioned before adding to the list
					if next_state != current_state:
						#tag state with pitch count and append
						current_state.batter_id = next_batter
						#we want to tag with the NEXT batter bc that is who bats during this game state!
						current_state.position_in_lineup_home,current_state.position_in_lineup_away,skip_game\
										= self._current_batter_position(current_state,home_roster,away_roster,next_batter)
						game_states.append(current_state)

						#update appropriate pitch count
						if current_batter != next_batter:
							#this is meaningless if we do not have any pitches yet - aka at gamestart
							if current_pitches is not None:
								#really though want to know what the state before it was,
								#as the pitcher in that state threw these pitches
								#subs can also happen on the first play...
								if len(game_states) < 2 or game_states[-2].inning.top:
									pitcher_appearance_home.pitches += current_pitches
								else:
									pitcher_appearance_away.pitches += current_pitches
							#update batter and appropriate roster
							skip_game = self._update_game_rosters(current_state,home_roster,away_roster,next_batter)
							current_batter = next_batter
					#update what state we are in and tag with necessary metadata
					current_state = next_state
					current_state.pitching_appearance_tracker_home = pitcher_appearance_home.deepcopy()
					current_state.pitching_appearance_tracker_away = pitcher_appearance_away.deepcopy()

					#update current_pitches
					current_pitches = next_pitches

				elif next.startswith("sub"):
					pitcher_appearance_home,pitcher_appearance_away,skip_game \
							= self._process_substitution(next,
														pitchers,
														pitching_substitutions,
														pitcher_appearance_home,
														pitcher_appearance_away,
														home_team,
														away_team,
														home_roster,
														away_roster,
														date,
														current_state)
				#update the play record for the next iteration
				next = self.data[self.iter_index].strip()
				self.iter_index += 1

			###########################################################################
			########### FINALIZE THE GAME #############################################
			#sometimes need to skip this game because of a parse error
			if skip_game:
				while not next.startswith("id") and self.iter_index < len(self.data):
					next = self.data[self.iter_index].strip()
					self.iter_index += 1
			else:
				#want to strip to make sure we don't have rando white space chars
				#add final pitchers to the dictionary, update pitch counts, add last state
				#do we append, idk? seems right
				if game_states[-1].inning.top:
					pitcher_appearance_home.pitches += current_pitches
				else:
					pitcher_appearance_away.pitches += current_pitches
				current_state.pitching_appearance_tracker_home = pitcher_appearance_home.deepcopy()
				current_state.pitching_appearance_tracker_away = pitcher_appearance_away.deepcopy()
				game_states.append(current_state)

				pitchers[pitcher_appearance_home.pitcher] = pitcher_appearance_home.to_pitching_appearance(current_state,True)
				pitchers[pitcher_appearance_away.pitcher] = pitcher_appearance_away.to_pitching_appearance(current_state,False)
				

				########################################################################
				######################### VERIFY AND YIELD #############################
				to_yield = game_model.Game(date,
										home_team.strip(),
										away_team.strip(),
										home_roster,
										away_roster,
										self.american_league,
										game_states,
										pitchers,
										pitching_substitutions)
				if self._verify_game(to_yield):
					yield to_yield

	#verify game-state progression to make sure weird thigns are not happening
	def _verify_game(self,to_verify):
		verified = True
		previous_state = None
		bases_empty = game_model.BaseRunners(False,False,False)
		for state in to_verify.game_progression:
			if previous_state is not None and state.inning > previous_state.inning:
				if state.outs != 0 or state.base_runners != bases_empty:
					verified = False
			if state.pitching_appearance_tracker_away is None or state.pitching_appearance_tracker_home is None:
				verified = False
			previous_state = state
		if self.debug and not verified:
			print "ERROR PARSING GAME - DID NOT PASS VERIFICATION\n" + repr(to_verify)
		return verified

	#update roster and lineup positions - includes err handling
	def _update_game_rosters(self,current_state,home_roster,away_roster,next_batter):
		skip_game = False
		#update batter and appropriate roster, NEXT BATTER CORRESPONDS TO CURRENT STATE - Be careful
		try:
			if current_state.inning.bottom:
				home_roster.last_batter(next_batter)
			else:
				away_roster.last_batter(next_batter)
		except error.RosterError as e:
			if self.debug:
				print "ROSTER ERROR - " + str(e)
			skip_game = True
		return skip_game

	def _process_substitution(self,
							next,
							pitchers,
							pitching_substitutions,
							pitcher_appearance_home,
							pitcher_appearance_away,
							home_team,
							away_team,
							home_roster,
							away_roster,
							date,
							current_state):
		skip_game = False
		player_sub_id,place_in_batting_order,home_team_sub,pitcher_sub = self._parse_substitution(next)
		#first, update pitching 
		if pitcher_sub:
			pitches = pitcher_appearance_home.pitches if home_team_sub \
						else pitcher_appearance_away.pitches
			if home_team_sub:
				pitchers[pitcher_appearance_home.pitcher] = pitcher_appearance_home.to_pitching_appearance(current_state,home_team_sub)
				pitcher_appearance_home = PitchingAppearanceTracker(date,current_state,player_sub_id)
			else:
				pitchers[pitcher_appearance_away.pitcher] = pitcher_appearance_away.to_pitching_appearance(current_state,home_team_sub)
				pitcher_appearance_away = PitchingAppearanceTracker(date,current_state,player_sub_id)
			
			try:
				sub_to_add = game_model.PitchingSubstitution(player_sub_id,
															home_team if home_team_sub else away_team,
															home_team_sub,
															current_state,
															pitches,
															away_roster.current_position() if home_team_sub else home_roster.current_position())
				pitching_substitutions[current_state] = sub_to_add
			except error.RosterError as e:
				skip_game = True
				if self.debug:
					print "ROSTER ERROR - " + str(e)
		#now adjust rosters
		if home_team_sub:
			home_roster.add(place_in_batting_order,player_sub_id)
		else:
			away_roster.add(place_in_batting_order,player_sub_id)

		return pitcher_appearance_home,pitcher_appearance_away,skip_game

	#includes error handling if the next play cannot be parsed
	def _try_to_parse_next(self,game_states,current_state,next):
		next_state,next_pitches,next_batter,skip_game = None,None,None,False
		try:
			next_state,next_pitches,next_batter = self._parse_play_code(current_state,next)
		except error.InvalidGameState as e:
			if self.debug:
				for s in game_states:
					print s
				print self.filename + " | Line " + str(self.iter_index) + " - " + e.message
			skip_game = True
		except error.ParseError as e:
			if self.debug:
				for s in game_states:
					print s
				print self.filename + " | Line " + str(self.iter_index) + " - " + e.message
			skip_game = True
		return next_state,next_pitches,next_batter,skip_game

	#get current batter position
	def _current_batter_position(self,current_state,home_roster,away_roster,batter_id):
		skip_game = False
		position_in_lineup_home,position_in_lineup_away = None,None
		try:
			#we want to tag with the NEXT batter bc that is who bats during this game state!
			position_in_lineup_away = away_roster.position(batter_id) if current_state.inning.top\
										else away_roster.current_position()
			position_in_lineup_home = home_roster.position(batter_id) if current_state.inning.bottom\
										else home_roster.current_position()
		except error.RosterError as e:
			skip_game = True
			if self.debug:
				print "ROSTER ERROR - " + str(e)

		return position_in_lineup_home,position_in_lineup_away,skip_game

	#get the next teams to play
	def _get_game_info(self):
		skip_game,home_team,away_team,start_home,start_away,roster_home,roster_away,date = False,None,None,None,None,None,None,None
		try:
			home_team,away_team,start_home,start_away,roster_home,roster_away,date = self._get_game_info_impl()
		except error.StartInfoError as e:
			print "START INFO ERROR - " + str(e)
		return skip_game,home_team,away_team,start_home,start_away,roster_home,roster_away,date

	#get the next teams to play
	def _get_game_info_impl(self):
		home_team,away_team,start_home,start_away,date,time = None,None,None,None,None,None
		home_roster,away_roster = game_model.GameRoster(),game_model.GameRoster()

		while not home_team or \
				not away_team or \
				not date or \
				not start_home or \
				not start_away or \
				not time or \
				not home_roster.full or \
				not away_roster.full:
			next = self.data[self.iter_index]
			self.iter_index += 1
			info = next.split(',')

			if info[0] == "info":
				if info[1] == "date":
					date = [int(i) for i in info[2].split('/')]
				elif info[1] == "starttime":
					t_d = [i.strip() for i in info[2].split(':')]
					if 'PM' in t_d[1] and int(t_d[0]) != 12:
						time = [int(t_d[0]) + 12,int(t_d[1][:-2])]
					else:
						time = [int(t_d[0]),int(t_d[1][:-2])]
				elif info[1] == "visteam":
					away_team = info[2]
				elif info[1] == "hometeam":
					home_team = info[2]
			elif info[0] == "start":
				if info[5].strip() == "1":
					if info[3] == "1":
						start_home = info[1]
					else:
						start_away = info[1]
				if info[3].strip() == "0":
					away_roster.add(int(info[4].strip()),info[1].strip())
				if info[3].strip() == "1":
					home_roster.add(int(info[4].strip()),info[1].strip())
			elif info[0] == "play":
				raise error.StartInfoError('{0} | {1} | {2}'.format(home_team,away_team,date))
		return home_team,away_team,start_home,start_away,home_roster,away_roster,GameTime(*(date + time))

	#return player_id_subbed,place_in_batting_order,which_team,pitcher?
	def _parse_substitution(self,code):	
		sub_info = code.split(",")
		return sub_info[1],int(sub_info[4]),sub_info[3] == '1',sub_info[5].strip() == '1'

	#returns next_state,pitches_thrown
	def _parse_play_code(self,current_state,code):
		previous_state = current_state
		current_state = current_state.transition_retrosheet(code)
		#tag current state with its transition code:
		current_state.transition_code = code

		#make sure inning never decreases
		if current_state.inning < previous_state.inning : 
			raise error.InvalidGameState("Cannot decrease inning from "\
											+ str(previous_state.inning)\
											+" to "\
											+ str(current_state.inning))
		
		#assuming parsing was okay, and we transitioned states,count pitches, get batter, and return
		split_code = code.split(",")

		return current_state,self._count_pitches(split_code[5]),split_code[3]

	#assumes that this is being given a pitch-code
	def _count_pitches(self,pitch_code):
		pitch_code = UNKNOWN_PITCH_CODE.sub("",pitch_code)
		pitch_code = CATCHER_PICKOFF.sub("",pitch_code)
		pitch_code = PITCHER_PICKOFF.sub("",pitch_code)
		return len(pitch_code)
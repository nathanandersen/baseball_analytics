# WIN EXPECTANCY TABLE - 
# class to represent win expectancy for a certain subset
# of all games. It is a dictionary with a few add ons
# by default it displays win expectancy from the point of view
# of the home team, but with a flag it can be flopped.
# can also be used to compute leverages

from game_model import *
import csv
import saber

__all__ = ["GameStateFrequencyTable","GameStateFrequencyTrackerTable"]

class GameStateFrequencyTrackerTable(dict):

	#takes a list of games, max inning, max score differential
	def __init__(self,compressed = True):
		dict.__init__(self)
		self.compressed = compressed
		self.total_states = 0

	def add_data_from_game_list(self,game_list):
		for game in game_list:
			prev = None
			for next in game.game_progression:
				if prev is not None:
					self.add_instance(prev,game.win(),next)
				prev = next

			#last state should have no transition
			self.add_instance(next,game.win(),None)

	#add gamestate occurences to the dictionarry
	def add_instance(self,game_state,home_win,next):
		if game_state not in self:
			self[game_state] = 0,0,saber.GameStateTransitionCounter()
		num_win,num_occ,trans_dict = self[game_state]
		trans_dict.add(next)
		self[game_state] = (num_win + 1,num_occ + 1,trans_dict) if home_win else (num_win,num_occ + 1,trans_dict)
		self.total_states += 1

	#returns None,None if the state is not in the dictionary
	#otherwise returns the win expectancy,sample size from the desired perspective
	def get_win_expectancy(self,game_state,home=True):
		if game_state in self:
			num_win,num_occ,_ = self[game_state]
			if num_occ == 0:
				return None,num_occ
			if home:
				return float(num_win) / float(num_occ),num_occ
			return 1 - float(num_win) / float(num_occ),num_occ
		return None,None

	def get_average_change_in_win_expectancy(self,game_state):
		win_exp,num_occ = self.get_win_expectancy(game_state)
		if win_exp is None:
			return None

		average = 0.0
		_,_,trans_dict = self[game_state]
		for state,ratio in trans_dict.iterate_transition_ratios():
			win_exp_a,_ = self.get_win_expectancy(game_state)
			win_exp_b,_ = self.get_win_expectancy(state)
			
			#transitioning to a None state indicates that
			#the current state is a game_over state - aka no effect on win expectancy
			#we do not really care about these states anyways
			if state is not None:
				average += ratio * abs(win_exp_a - win_exp_b)
		return average

	def as_game_state_frequency_table(self):
		#first we want to convert to an intermediate representation
		#game state -> frequency,win expectancy,average change in win expectancy
		intermediate_dict = {}

		for state in self:
			win_exp,freq = self.get_win_expectancy(state)
			intermediate_dict[state] = freq,win_exp,self.get_average_change_in_win_expectancy(state)
	
		#now build the final game state frequency table
		global_average_change_win_exp = 0.0
		for state in intermediate_dict:
			freq,_,average_change = intermediate_dict[state]
			global_average_change_win_exp += (float(freq) / float(self.total_states)) * average_change

		g = GameStateFrequencyTable(self.total_states,global_average_change_win_exp)

		for state in intermediate_dict:
			g[state] = intermediate_dict[state]

		return g

#just a nice wrapper class, all heavy lifting is done before this stage
#should have a tuple of frequency,win_exp,average_change,leverage
class GameStateFrequencyTable(dict):

	def __init__(self,total_states,average_change_win_expectancy):
		dict.__init__(self)
		self.total_states = total_states
		self.average_change_win_expectancy = average_change_win_expectancy

	def get_win_expectancy(self,game_state,home=True):
		if game_state in self:
			_,win_exp,_ = self[game_state]
			if home:
				return win_exp
			return 1 - win_exp
		return None

	def get_leverage(self,game_state):
		if game_state in self:
			_,_,average_change = self[game_state]
			return average_change / self.average_change_win_expectancy
		return None

	def get_frequency(self,game_state):
		if game_state in self:
			f,_,_ = self[game_state]
			return f
		return None

	#print out the win expectancy table in ueful format
	#chooses a maximal printing bound based on fields and parameters
	def write_table_as_csv(self,filename,start_inning,end_inning,score_differential,perspective_home = True):
		#make sure at least some basic conditions are met
		if start_inning >= end_inning or start_inning < 1 or score_differential < 0:
			return
		#figure out the printing bounds based on input and fields

		with open(filename,'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			#iterate through acceptable states in order and print csv of state + win expectancy
			for inn_num in range(start_inning,end_inning+1):
				for tb in range(2):
					#convert tb to bool
					tb = False if tb == 0 else True
					for sd in range(-score_differential,score_differential+1):
						#create equivalence class game scores
						score_away,score_home = None,None
						if sd < 0:
							score_away = abs(sd)
							score_home = 0
						else:
							score_away = 0
							score_home = sd
						for num_outs in range(3):
							for base_runners in BaseRunners.enumerate_combinations():
								#make gamestate
								state = GameState(score_home,score_away,Inning(inn_num,bottom = tb),num_outs,base_runners)
								#print win expectancies
								win_exp = self.get_win_expectancy(state,home = perspective_home)
								leverage = self.get_leverage(state)
								frequency = self.get_frequency(state)
								win_exp = str(win_exp) if win_exp is not None else "UNDEFINED"
								frequency = str(frequency) if frequency is not None else "0"
								row = state.to_list()
								row.append(frequency)
								row.append(win_exp)
								row.append(leverage)
								csvwriter.writerow(row)

	def write_table_latex(self,filename,start_inning,end_inning,score_differential,perspective_home=True):
		#make sure at least some basic conditions are met
		if start_inning >= end_inning or start_inning < 1 or score_differential < 0:
			return
		#figure out the printing bounds based on input and fields

		with open(filename,'wb') as outfile:
			#iterate through acceptable states in order and print csv of state + win expectancy
			for inn_num in range(start_inning,end_inning+1):
				for tb in range(2):
					#convert tb to bool
					tb = False if tb == 0 else True
					for sd in range(-score_differential,score_differential+1):
						#create equivalence class game scores
						score_away,score_home = None,None
						if sd < 0:
							score_away = abs(sd)
							score_home = 0
						else:
							score_away = 0
							score_home = sd
						for num_outs in range(3):
							for base_runners in BaseRunners.enumerate_combinations():
								#make gamestate
								state = GameState(score_home,score_away,Inning(inn_num,bottom = tb),num_outs,base_runners)
								#print win expectancies
								leverage = self.get_leverage(state)
								row = state.to_list()
								row.append(leverage)
								row = [str(i) for i in row]
								row_string = " & ".join(row)
								row_string = row_string + " \\\\ \\hline \n"
								outfile.write(row_string)
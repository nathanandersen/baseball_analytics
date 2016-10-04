# RUNNER MOTION - 
#class to handle runner motion and aid in processing of play
#presence in the dictionary means that there is a runner on that
#base and value in the key,value pair signifies end base after
#the play. -1 signals runner is put out (or batter)
# based on this info the number of outs incurred or runs scored
# on this movement of runnners can be computed.

__all__=["RunnerMotion"]

import game_model

class RunnerMotion(dict):
	def __init__(self,runner_start):
		self[0] = 0
		if runner_start.first:
			self[1] = 1
		if runner_start.second:
			self[2] = 2
		if runner_start.third:
			self[3] = 3

	def get_result_of_motion(self):
		runs_scored,outs_incurred = 0,0
		first,second,third = False,False,False

		for _,v in self.iteritems():
			if v == -1:
				outs_incurred += 1
			elif v == 1 :
				first = True
			elif v == 2: 
				second = True
			elif v == 3:
				third = True
			elif v == 4:
				runs_scored += 1

		return runs_scored,outs_incurred,game_model.BaseRunners(first,second,third)
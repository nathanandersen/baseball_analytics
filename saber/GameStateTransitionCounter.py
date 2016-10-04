# GAME STATE TRANSITION COUNTER - 
# indexed by tuples 

__all__ = ["GameStateTransitionCounter"]

class GameStateTransitionCounter(object):

	def __init__(self):
		self.total = 0
		self.subsequent_states = {}

	def add(self,state):
		transitions = self.subsequent_states[state] if state in self.subsequent_states else 0
		self.subsequent_states[state] = transitions + 1
		self.total += 1

	def iterate_transition_ratios(self):
		if self.total == 0:
			return
		for state in self.subsequent_states:
			yield state,float(self.subsequent_states[state]) / float(self.total)
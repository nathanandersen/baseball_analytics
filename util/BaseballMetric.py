# The alternative Baseball metric

__all__ = ["baseball_confusion_matrix"]

class BasicBlock(object):
	def __init__(self,prediction):
		self.states = []
		self.prediction = prediction

	def add_state(self,state):
		self.states.append(state)


# performs the measurement

def baseball_confusion_matrix(clf):
	pass
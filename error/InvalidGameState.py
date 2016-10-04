#INVALID GAME STATE - error thrown when a game state is not valid

class InvalidGameState(Exception):
	def __init__(self, message =''):
		self.message = message

	def __str__(self):
		return self.message


class InvalidScoreError(InvalidGameState):
	pass

class InvalidOutsError(InvalidGameState):
	pass

class InvalidInningError(InvalidGameState):
	pass
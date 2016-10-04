# INNING NUMBER - Needs to be able to support addition and 

import fractions

__all__ = ["InningNumber"]

class InningNumber(object):

	def __init__(self,innings,partial_innings):
		self.innings = innings + partial_innings / 3

		self.partial_innings = partial_innings % 3

	def __str__(self):
		return str(self.innings) + "." + str(self.partial_innings)

	def __repr__(self):
		return self.__str__()

	def __add__(self,other):
		return InningNumber(self.innings + other.innings,self.partial_innings + other.partial_innings)

	def __float__(self):
		return float(self.innings) + (self.float(partial_innings) / 3)
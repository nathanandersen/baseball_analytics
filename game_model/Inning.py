# INNING - 
# wraps an int, needed because no good way to treat
# innings natively in python. Inning reps start at 0
# want to keep minimal information around - pickling

__all__ = ["Inning"]

class Inning(object) :

	def __init__(self,inning_number,bottom = False):
		self.inning_rep = (inning_number - 1) * 2
		if bottom : 
			self.inning_rep = self.inning_rep + 1

	#representational methods
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		half = "Top " if self.inning_rep % 2 == 0 else "Bottom "
		return half + str(self.inning_rep / 2 + 1)

	#relational methods
	def __eq__(self,other):
		return isinstance(other,self.__class__) and other.inning_rep == self.inning_rep
	def __ne__(self,other):
		return isinstance(other,self.__class__) and other.inning_rep != self.inning_rep
	def __lt__(self,other):
		return isinstance(other,self.__class__) and self.inning_rep < other.inning_rep
	def __gt__(self,other):
		return isinstance(other,self.__class__) and self.inning_rep > other.inning_rep
	def __ge__(self,other):
		return not self.__lt__(other)
	def __le__(self,other):
		return not self.__gt__(other)

	def next(self):
		return Inning.from_inning_rep(self.inning_rep + 1)

	#which half of the inning is it?
	@property
	def top(self):
		return self.inning_rep % 2 == 0
	@property
	def bottom(self):
		return self.inning_rep % 2 == 1

	@property
	def number(self):
		return self.inning_rep / 2 + 1

	@classmethod
	def start(cls):
		return Inning(1,False)

	@classmethod
	def from_inning_rep(cls,inning_rep):
		inn = Inning(1)
		inn.inning_rep = inning_rep
		return inn
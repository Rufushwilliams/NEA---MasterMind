class Statistics:
	"""
	Statistics class that stores the statistics of a human player
	"""
	def __init__(self):
		pass

	def getStats(self):
		pass

	def setStats(self):
		pass



class Player:
	"""
	Basic player class
	"""

	def __init__(self):
		pass

	def getMove(self):
		pass



class AI(Player):
	"""
	AI class that inherits from the Player class
	"""
	def __init__(self):
		super.__init__(self)
		pass


class Human(Player):
	"""
	Human class that inherits from the Player class
	"""
	def __init__(self, statistics:Statistics):
		super.__init__(self)
		self.statistics = statistics
		pass


class LocalHuman(Human):
	"""
	Local human class that inherits from the Human class
	"""
	def __init__(self):
		super.__init__(self)
		pass

class NetworkingHuman(Human):
	"""
	Networking human class that inherits from the Human class
	"""
	def __init__(self):
		super.__init__(self)
		pass



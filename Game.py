from Player import Player

class Game:
	"""
	A class that represents the game
	"""
	def __init__(self, player1:Player, player2:Player):
		self.player1 = player1
		self.player2 = player2
		self.currentPlayer = player1
		self.winner = None

	def createBoard(self):
		"""
		Creates a board
		"""
		pass

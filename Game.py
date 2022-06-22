from Player import Player



class Board:
	"""
	Board class
	"""
	def __init__(self, length:int, colours:dict, totalGuesses:int=6):
		self.__colours = colours
		self.__lenOfGuess = length
		self.__totalGuesses = totalGuesses
	
	def getColours(self):
		return self.__colours
	
	def getLenOfGuess(self):
		return self.__lenOfGuess
	
	def getTotalGuesses(self):
		return self.__totalGuesses

	def getRemainingGuesses(self):
		return self.__totalGuesses - len(self.getGuesses())
	
	def makeGuess(self, guess:list) -> list:
		"""
		Makes a guess and returns a list of the result
		"""
		raise NotImplementedError()

	def getGuesses(self) -> list:
		"""
		returns the already made guesses
		"""
		if self.__guesses:
			return self.__guesses
		else:
			return None
	
	def __str__(self) -> str:
		"""
		Returns a string representation of the board
		"""
		raise NotImplementedError()




class Game:
	"""
	A class that represents the game
	"""
	def __init__(self, player1:Player, player2:Player, length:int, colours:dict, numGuesses:int):
		self.player1 = player1
		self.player2 = player2
		self.currentPlayer = player1
		self.winner = None
		self.board = self.createBoard(length, colours, numGuesses)

	def createBoard(self, length:int, colours:dict, numGuesses) -> Board:
		"""
		Creates and returns a board
		"""
		raise NotImplementedError()

from Player import Player
from Board import Board


class Game:
    """
    A class that represents the game
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        length: int,
        numGuesses: int,
        numRounds: int,
        duplicatesAllowed: bool,
        colours: dict[int, str],
    ):
        self.__player1 = player1
        self.__player2 = player2
        self.__currentPlayer = player1
        self.__numRounds = numRounds
        self.__player1RoundWins = 0
        self.__player2RoundWins = 0
        self.__winner = None
        self.__board = self.__createBoard(
            length, numGuesses, duplicatesAllowed, colours
        )

    def __createBoard(
        self, length: int, numGuesses: int, duplicatesAllowed: bool, colours: dict
    ) -> Board:
        """
        Creates and returns a board
        """
        return Board(
            length=length,
            totalGuesses=numGuesses,
            duplicatesAllowed=duplicatesAllowed,
            colours=colours,
        )

    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer

    def getBoard(self) -> Board:
        return self.__board

    def getWinner(self) -> Player:
        return self.__winner  # type: ignore [return-value] # mypy cannot detect that self.__winner will be a Player

    def switchPlayer(self):
        """
        Switches the current player
        """
        if self.__currentPlayer == self.__player1:
            self.__currentPlayer = self.__player2
        else:
            self.__currentPlayer = self.__player1

    def getNextGuess(self) -> list:
        """
        Returns the current players next guess
        """
        return self.__currentPlayer.getMove()

    def setBoardCode(self, code: list | None = None):
        """
        Sets the board code. If code is None, a random code is generated
        """
        self.__board.setCode(code)

    def makeGuess(self, guess: list) -> tuple[list, int, bool]:
        """
        Gets a move from the current player and makes a guess. Returns a tuple of the result, the number of guesses remaining, if the guess was correct
        """
        return self.__board.makeGuess(guess)

    def playGameRound(self):
        """
        Plays a round of the game.
        """
        while self.__winner is None:
            nextMove = self.getNextGuess()
            result, remainingGuesses, codeCorrect = self.makeGuess(nextMove)
            if codeCorrect:
                self.__winner = self.__currentPlayer
                break
            if remainingGuesses == 0:
                if self.__currentPlayer == self.__player1:
                    self.__winner = self.__player2
                else:
                    self.__winner = self.__player1
            self.displayBoard()
        self.displayBoard()
        self.displayWinner()

    def displayBoard(self):
        """
        Displays the board to the ui.
        Calls the current player's displayBoard method
        """
        self.__currentPlayer.displayBoard(self.__board)

    def displayGuess(self, guess: list, result: list):
        """
        Displays the guess and result to the ui.
        Calls the current player's displayGuess method
        """
        self.__currentPlayer.displayGuess(guess, result)

    def displayWinner(self):
        """
        Displays the winner to the ui.
        Calls the current player's displayWinner method
        """
        self.__currentPlayer.displayWinner(self.__winner)

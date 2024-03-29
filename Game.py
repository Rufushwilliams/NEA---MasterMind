from time import time

from Board import Board
from Player import Player, Terminal


class Game:
    """
    A class that represents the game
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        length: int = 4,
        numGuesses: int = 6,
        numRounds: int = 3,
        duplicatesAllowed: bool = True,
        colourNum: int = 6,
    ):
        self.__player1 = player1
        self.__player2 = player2
        self.__currentPlayer = player1
        self.__length = length
        self.__numGuesses = numGuesses
        self.__numRounds = numRounds
        self.__duplicatesAllowed = duplicatesAllowed
        self.__colourNum = colourNum
        self.__player1RoundWins = 0
        self.__player2RoundWins = 0
        self.__winner = None
        self.__board = None

    def __createBoard(
        self,
        length: int,
        numGuesses: int,
        duplicatesAllowed: bool,
        colourNum: int,
    ) -> Board:
        """
        Creates and returns a board
        """
        ################################################
        # GROUP A SKILL: DYNAMIC GENERATION OF OBJECTS #
        ################################################
        return Board(
            length=length,
            totalGuesses=numGuesses,
            duplicatesAllowed=duplicatesAllowed,
            colourNum=colourNum,
        )

    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer

    def getPlayer1(self) -> Player:
        return self.__player1

    def getPlayer2(self) -> Player:
        return self.__player2

    def getLengthOfCode(self) -> int:
        return self.__length

    def getNumGuesses(self) -> int:
        return self.__numGuesses

    def getNumRounds(self) -> int:
        return self.__numRounds

    def getColourNum(self) -> int:
        return self.__colourNum

    def getDuplicatesAllowed(self) -> bool:
        return self.__duplicatesAllowed

    def getBoard(self) -> Board:
        return self.__board

    def getWinner(self) -> Player | None:
        return self.__winner

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
        return self.__currentPlayer.getMove(self.__board)

    def setBoardCode(self, random: bool = False):
        """
        Sets the board code.
        Gets the code from the player who's turn it is not.
        """
        if not random:
            if self.__currentPlayer == self.__player1:
                self.__board.setCode(self.__player2.getCode(self.__board))
            else:
                self.__board.setCode(self.__player1.getCode(self.__board))
        else:
            self.__board.setCode()

    def makeGuess(self, guess: list) -> tuple[list, int, bool]:
        """
        Gets a move from the current player and makes a guess. Returns a tuple of the result, the number of guesses remaining, if the guess was correct
        """
        return self.__board.makeGuess(guess)

    def playGameRound(self):
        """
        Plays a round of the game.
        """
        self.__board = self.__createBoard(
            self.__length, self.__numGuesses, self.__duplicatesAllowed, self.__colourNum
        )
        self.setBoardCode()
        roundWinner = None
        while roundWinner is None:
            nextMove = self.getNextGuess()
            result, remainingGuesses, codeCorrect = self.makeGuess(nextMove)
            if codeCorrect:
                roundWinner = self.__currentPlayer
                break
            if remainingGuesses == 0:
                if self.__currentPlayer == self.__player1:
                    roundWinner = self.__player2
                else:
                    roundWinner = self.__player1
                break
            self.displayBoard()
        self.displayBoard(self.__board.getCode())
        self.displayRoundWinner(roundWinner)
        # add 1 to the winner's round win count
        if roundWinner == self.__player1:
            self.__player1RoundWins += 1
        else:
            self.__player2RoundWins += 1

    def displayBoard(self, code: list = None):
        """
        Displays the board to the ui.
        Calls both players' displayBoard method
        """
        if type(self.__player1) == Terminal and type(self.__player2) == Terminal:
            self.__player1.displayBoard(self.__board, code)
        else:
            self.__player1.displayBoard(self.__board, code)
            self.__player2.displayBoard(self.__board, code)

    def displayRoundWinner(self, roundWinner: Player):
        """
        Displays the winner of the round to the ui.
        Calls both players' displayRoundWinner method
        """
        winnerName = roundWinner.getUsername()
        if type(self.__player1) == Terminal and type(self.__player2) == Terminal:
            self.__player1.displayRoundWinner(winnerName)
        else:
            self.__player1.displayRoundWinner(winnerName)
            self.__player2.displayRoundWinner(winnerName)

    def displayWinner(self):
        """
        Displays the winner to the ui.
        Calls both players' displayWinner method
        """
        winnerName = self.__winner.getUsername() if self.__winner is not None else None
        if type(self.__player1) == Terminal and type(self.__player2) == Terminal:
            self.__player1.displayWinner(winnerName)
        else:
            self.__player1.displayWinner(winnerName)
            self.__player2.displayWinner(winnerName)

    def displayRoundNumber(self, roundNumber: int):
        """
        Displays the round number to the ui.
        Calls both players' displayRoundNumber method
        """
        if type(self.__player1) == Terminal and type(self.__player2) == Terminal:
            self.__player1.displayRoundNumber(roundNumber)
        else:
            self.__player1.displayRoundNumber(roundNumber)
            self.__player2.displayRoundNumber(roundNumber)

    def updatePlayerStats(self, timePlayed: float = None):
        """
        Updates the players' stats
        """
        winner = None
        if self.__winner:
            winner = self.__winner.getUsername()
        self.__player1.updateStats(winner, self.__numRounds, timePlayed)
        self.__player2.updateStats(winner, self.__numRounds, timePlayed)

    def run(self):
        """
        Runs the game and returns a tuple of the time taken to run and if player1 won
        """
        startTime = time()
        for i in range(self.__numRounds):
            self.displayRoundNumber(i + 1)
            self.playGameRound()
            self.switchPlayer()
        if self.__player1RoundWins > self.__player2RoundWins:
            self.__winner = self.__player1
        elif self.__player1RoundWins < self.__player2RoundWins:
            self.__winner = self.__player2
        else:
            self.__winner = None
        self.displayWinner()
        endTime = time()
        self.__gameTime = round(endTime - startTime, 2)
        self.updatePlayerStats(self.__gameTime)
        return (self.__gameTime, self.__winner == self.__player1)

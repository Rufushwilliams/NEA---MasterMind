from Player import Player, Terminal
from Board import Board


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
        return Board(
            length=length,
            totalGuesses=numGuesses,
            duplicatesAllowed=duplicatesAllowed,
            colourNum=colourNum,
        )

    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer

    def getBoard(self) -> Board:
        return self.__board

    def getWinner(self) -> Player:
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
        return self.__currentPlayer.getMove(
            self.__board.getLenOfGuess(),
            len(self.__board.getColours()),
            self.__board.getDuplicatesAllowed(),
        )

    def setBoardCode(self, random: bool = False):
        """
        Sets the board code.
        Gets the code from the player who's turn it is not.
        """
        if not random:
            if self.__currentPlayer == self.__player1:
                self.__board.setCode(
                    self.__player2.getCode(
                        self.__board.getLenOfGuess(),
                        len(self.__board.getColours()),
                        self.__board.getDuplicatesAllowed(),
                    )
                )
            else:
                self.__board.setCode(
                    self.__player1.getCode(
                        self.__board.getLenOfGuess(),
                        len(self.__board.getColours()),
                        self.__board.getDuplicatesAllowed(),
                    )
                )
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
        self.displayBoard()
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
        if type(self.__player1) == Terminal and type(self.__player2) == Terminal:
            self.__player1.displayRoundWinner(roundWinner)
        else:
            self.__player1.displayRoundWinner(roundWinner)
            self.__player2.displayRoundWinner(roundWinner)

    def displayWinner(self):
        """
        Displays the winner to the ui.
        Calls both players' displayWinner method
        """
        if type(self.__player1) == Terminal and type(self.__player2) == Terminal:
            self.__player1.displayWinner(self.__winner)
        else:
            self.__player1.displayWinner(self.__winner)
            self.__player2.displayWinner(self.__winner)

    def run(self):
        """
        Runs the game
        """
        for i in range(self.__numRounds):
            print("------------------------------")
            print("Round " + str(i + 1))
            print("------------------------------")
            self.playGameRound()
            self.switchPlayer()
        if self.__player1RoundWins > self.__player2RoundWins:
            self.__winner = self.__player1
        elif self.__player1RoundWins < self.__player2RoundWins:
            self.__winner = self.__player2
        else:
            self.__winner = None
        self.displayWinner()

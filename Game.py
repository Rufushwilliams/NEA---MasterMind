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
        length: int = 4,
        numGuesses: int = 6,
        numRounds: int = 1,
        duplicatesAllowed: bool = False,
        colours: dict[int, str] = None,
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
        self,
        length: int,
        numGuesses: int,
        duplicatesAllowed: bool,
        colours: dict[int, str] | None,
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
        return self.__currentPlayer.getMove(
            self.__board.getLenOfGuess(), self.__board.getColours()
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
                        self.__board.getLenOfGuess(), self.__board.getColours()
                    )
                )
            else:
                self.__board.setCode(
                    self.__player1.getCode(
                        self.__board.getLenOfGuess(), self.__board.getColours()
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
            self.displayBoard()
        if remainingGuesses != 0:
            self.displayBoard()
        self.displayRoundWinner(roundWinner)
        # add 1 to the winner's round win count
        if roundWinner == self.__player1:
            self.__player1RoundWins += 1
        else:
            self.__player2RoundWins += 1

    def displayBoard(self):
        """
        Displays the board to the ui.
        Calls both players' displayBoard method
        """
        self.__player1.displayBoard(self.__board)
        self.__player2.displayBoard(self.__board)

    def displayRoundWinner(self, roundWinner: Player):
        """
        Displays the winner of the round to the ui.
        Calls both players' displayRoundWinner method
        """
        self.__player1.displayRoundWinner(roundWinner)
        self.__player2.displayRoundWinner(roundWinner)

    def displayWinner(self):
        """
        Displays the winner to the ui.
        Calls both players' displayWinner method
        """
        self.__player1.displayWinner(self.__winner)
        self.__player2.displayWinner(self.__winner)

    def run(self):
        """
        Runs the game
        """
        for i in range(self.__numRounds):
            print("------------------------------")
            print("Round " + str(i + 1))
            self.playGameRound()
            self.switchPlayer()
        if self.__player1RoundWins > self.__player2RoundWins:
            self.__winner = self.__player1
        elif self.__player1RoundWins < self.__player2RoundWins:
            self.__winner = self.__player2
        else:
            self.__winner = None
        self.displayWinner()

import random
from Player import Player


class Board:
    """
    Board class
    """

    __COLOURS = {
        1: "red",
        2: "blue",
        3: "green",
        4: "yellow",
        5: "orange",
        6: "purple",
    }
    __RESULTCOLOURS = {1: "black", 2: "white"}

    def __init__(
        self,
        length: int,
        totalGuesses: int = 6,
        duplicatesAllowed: bool = False,
        colours: dict[int, str] = __COLOURS,
        resultColours: dict[int, str] = __RESULTCOLOURS,
    ):
        self.__lenOfGuess = length
        self.__totalGuesses = totalGuesses
        self.__duplicatesAllowed = duplicatesAllowed
        self.__colours = colours
        self.__resultColours = resultColours
        self.__guessPointer = 0
        self.__guesses: list[list[int | None]] = [
            [None for _ in range(length)] for _ in range(totalGuesses)
        ]
        self.__code: list[int] | None = None

    def getColours(self):
        return self.__colours

    def getResultColours(self):
        return self.__resultColours

    def getLenOfGuess(self):
        return self.__lenOfGuess

    def getTotalGuesses(self):
        return self.__totalGuesses

    def getRemainingGuesses(self):
        return self.__totalGuesses - self.__guessPointer

    def makeGuess(self, guess: list) -> tuple[list, int, bool]:
        """
        Makes a guess and returns a tuple containing the result, the number of guesses remaining, if the guess was correct
        """
        self.__guesses[self.__guessPointer] = guess
        result = self.__genGuessResult(guess)
        if result == [1] * self.__lenOfGuess:
            codeCorrect = True
        else:
            codeCorrect = False
            self.__guessPointer += 1
        return (result, self.getRemainingGuesses(), codeCorrect)

    def __genGuessResult(self, guess: list[int]) -> list:
        """
        Returns a list of the result of a guess
        """
        # checks that the guess is in the correct format
        if self.__code == None:
            raise ValueError("Code is not set")
        elif len(guess) != self.__lenOfGuess:
            raise ValueError("Guess length is not long enough")
        elif not all(num in list(self.__colours.keys()) for num in guess):
            raise ValueError("Guess contains invalid colour")
        else:
            # calculates the result
            result = []
            tempCode = self.__code.copy()  # type: ignore
            tempGuess = guess.copy()
            for i in range(len(guess)):
                if self.__code[i] == guess[i]:  # type: ignore
                    result.append(1)
                    tempCode[i] = None  # type: ignore
                    tempGuess[i] = None  # type: ignore
            tempGuess = [x for x in tempGuess if x is not None]
            tempCode = [x for x in tempCode if x is not None]
            for i in range(len(tempGuess)):
                if tempGuess[i] in tempCode:
                    result.append(2)
                    tempCode.pop(tempCode.index(tempGuess[i]))
            return result

    def getGuesses(self) -> list[list[int]]:
        """
        returns the already made guessess
        """
        guesses = []
        for i in range(self.__guessPointer):
            guesses.append(self.__guesses[i])
        return guesses  # type: ignore [return-value] # mypy cannot detect that guesses will contain only integers

    def setCode(self, code: list | None = None):
        """
        Sets the code for the board
        """
        if code is None:
            # generate random code
            if not self.__duplicatesAllowed:
                self.__code = random.sample(
                    list(self.__colours.keys()), self.__lenOfGuess
                )
            else:
                self.__code = [
                    random.choice(list(self.__colours.keys()))
                    for _ in range(self.__lenOfGuess)
                ]
        else:
            if len(code) != self.__lenOfGuess:
                raise ValueError("Code length is not correct")
            elif not all(colour in self.__colours for colour in code):
                raise ValueError("Code contains invalid colour")
            elif not self.__duplicatesAllowed and len(set(code)) != self.__lenOfGuess:
                raise ValueError("Code contains duplicates")
            else:
                self.__code = code

    def getCode(self) -> list | None:
        return self.__code

    def __str__(self) -> str:
        """
        Returns a string representation of the board
        """
        raise NotImplementedError()


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
            if remainingGuesses == 0:
                if self.__currentPlayer == self.__player1:
                    self.__winner = self.__player2
                else:
                    self.__winner = self.__player1
            self.displayGuess(nextMove, result)
        self.displayWinner()

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

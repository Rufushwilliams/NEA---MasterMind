import random
from Player import Player


class Board:
    """
    Board class
    """

    def __init__(
        self,
        length: int,
        totalGuesses: int = 6,
        duplicatesAllowed: bool = False,
        colours: dict = {
            1: "red",
            2: "blue",
            3: "green",
            4: "yellow",
            5: "orange",
            6: "purple",
        },
        resultColours: dict = {1: "black", 2: "white"},
    ):
        self.__lenOfGuess = length
        self.__totalGuesses = totalGuesses
        self.__duplicatesAllowed = duplicatesAllowed
        self.__colours = colours
        self.__resultColours = resultColours
        self.__guessPointer = 0
        self.__guesses = [[None for _ in range(length)] for _ in range(totalGuesses)]
        self.__code = None

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

    def makeGuess(self, guess: list) -> tuple:
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

    def __genGuessResult(self, guess: list) -> list:
        """
        Returns a list of the result of a guess
        """
        # checks that the guess is in the correct format
        if len(guess) != self.__lenOfGuess:
            raise ValueError("Guess length is not long enough")
        elif not all(num in list(self.__colours.keys()) for num in guess):
            raise ValueError("Guess contains invalid colour")
        # calculates the result
        result = []
        for i in range(len(guess)):
            if guess[i] == self.__code[i]:
                result.append(1)
            elif guess[i] in self.__code:
                result.append(2)
        return result
        # DOES NOT WORK FOR DUPLICATES

    def getGuesses(self) -> list:
        """
        returns the already made guesses
        """
        guesses = []
        for i in range(self.__guessPointer):
            guesses.append(self.__guesses[i])
        return guesses

    def setCode(self, code: list = None):
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
            
    def getCode(self) -> list:
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
        duplicatesAllowed: bool,
        colours: dict,
    ):
        self.__player1 = player1
        self.__player2 = player2
        self.__currentPlayer = player1
        self.__winner = None
        self.__board = self.__createBoard(length, numGuesses, duplicatesAllowed, colours)

    def __createBoard(self, length: int, numGuesses: int, duplicatesAllowed: bool, colours: dict) -> Board:
        """
        Creates and returns a board
        """
        return Board(length = length, totalGuesses = numGuesses, duplicatesAllowed = duplicatesAllowed, colours = colours)

    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer

    def makeGuess(self, guess: list) -> tuple:
        """
        Makes a guess and returns a list of the result
        """
        return self.__board.makeGuess(guess)

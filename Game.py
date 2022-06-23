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
        colours: dict[int, str] = {
            1: "red",
            2: "blue",
            3: "green",
            4: "yellow",
            5: "orange",
            6: "purple",
        },
        resultColours: dict[int, str] = {1: "black", 2: "white"},
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
            assert (
                self.__code is not None
            )  # mypy bug -> tells mypy that self.__code is not None
            result = []
            for i in range(len(guess)):
                if guess[i] == self.__code[i]:
                    result.append(1)
                elif guess[i] in self.__code:
                    result.append(2)
            return result
            # DOES NOT WORK FOR DUPLICATES

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
        duplicatesAllowed: bool,
        colours: dict,
    ):
        self.__player1 = player1
        self.__player2 = player2
        self.__currentPlayer = player1
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

    def switchPlayer(self):
        """
        Switches the current player
        """
        if self.__currentPlayer == self.__player1:
            self.__currentPlayer = self.__player2
        else:
            self.__currentPlayer = self.__player1

    def makeGuess(self) -> tuple[list, int, bool]:
        """
        Gets a move from the current player and makes a guess
        """
        guess = self.__currentPlayer.getMove()
        return self.__board.makeGuess(guess)

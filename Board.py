from random import sample, choice


class Board:
    """
    Board class
    """

    def __init__(
        self,
        length: int = 4,
        totalGuesses: int = 6,
        duplicatesAllowed: bool = True,
        colourNum: int = 6,
        resultNums: list[int] = [1, 2],
    ):
        self.__lenOfGuess = length
        self.__totalGuesses = totalGuesses
        self.__duplicatesAllowed = duplicatesAllowed
        self.__colourNums = [i for i in range(1, colourNum+1)]
        self.__resultNums = resultNums
        self.__guessPointer = 0
        self.__guesses: list[list[int | None]] = [
            [None for _ in range(length)] for _ in range(totalGuesses)
        ]
        self.__results: list[list[int | None]] = [
            [None for _ in range(length)] for _ in range(totalGuesses)
        ]
        self.__code: list[int] | None = None

    def getColours(self):
        return self.__colourNums

    def getResultColours(self):
        return self.__resultNums

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
        self.__results[self.__guessPointer] = result
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
        elif not all(num in self.__colourNums for num in guess):
            raise ValueError("Guess contains invalid colour")
        else:
            # calculates the result
            result = []
            tempCode = self.__code.copy()
            tempGuess = guess.copy()
            for i in range(len(guess)):
                if self.__code[i] == guess[i]:
                    result.append(1)
                    tempCode[i] = None
                    tempGuess[i] = None
            tempGuess = [x for x in tempGuess if x is not None]
            tempCode = [x for x in tempCode if x is not None]
            for i in range(len(tempGuess)):
                if tempGuess[i] in tempCode:
                    result.append(2)
                    tempCode.pop(tempCode.index(tempGuess[i]))
            return result

    def getGuesses(self) -> list[list[int]]:
        """
        Returns the already made guessess
        """
        guesses = []
        for i in range(self.__guessPointer):
            guesses.append(self.__guesses[i])
        return guesses

    def getResults(self) -> list[list[int]]:
        """
        Returns the results of the guesses
        """
        results = []
        for i in range(self.__guessPointer):
            results.append(self.__results[i])
        return results

    def setCode(self, code: list[int] | None = None):
        """
        Sets the code for the board.
        If no code is given, a random code is generated
        """
        if code is None:
            # generate random code
            if not self.__duplicatesAllowed:
                self.__code = sample(self.__colourNums, self.__lenOfGuess)
            else:
                self.__code = [
                    choice(self.__colourNums)
                    for _ in range(self.__lenOfGuess)
                ]
        else:
            if len(code) != self.__lenOfGuess:
                raise ValueError("Code length is not correct")
            elif not all(colour in self.__colourNums for colour in code):
                raise ValueError("Code contains invalid colour")
            elif not self.__duplicatesAllowed and len(set(code)) != self.__lenOfGuess:
                raise ValueError("Code contains duplicates")
            else:
                self.__code = code

    def getCode(self) -> list | None:
        return self.__code

    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        Does not show the code.
        """
        guesses = self.getGuesses()
        results = self.getResults()
        output = ""
        output += "-------------------------------------------------------" + "\n"
        for i in range(len(guesses)):
            output += str(guesses[i]) + "  " + str(results[i]) + "\n"
        output += "Remaining guesses: " + str(self.getRemainingGuesses()) + "\n"
        output += "-------------------------------------------------------"
        return output

import random


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
    
    def getCode(self):
        return self.__code

    def __str__(self) -> str:
        """
        Returns a string representation of the board
        """
        raise NotImplementedError()



print("Welcome to Mastermind!")
print("Getting a 1 in the result means that you have a peg in the correct colour and position.")
print("Getting a 2 in the result means that you have a peg in the correct colour but in the wrong position.")
print("Generating the code...")
board = Board(4, 6)
board.setCode()
while True:
    while True:
        guess = input("Enter a guess in the form _ _ _ _ : ")
        if guess == "show code":
            print(board.getCode())
            continue
        guess = guess.split(" ")
        guess = [int(i) for i in guess]
        if len(guess) != board.getLenOfGuess():
            print("Guess length is not long enough")
        elif not all(num in list(board.getColours().keys()) for num in guess):
            print("Guess contains invalid number")
        else:
            break
    result, remainingGuesses, codeCorrect = board.makeGuess(guess)
    print(result)
    if codeCorrect:
        print("You win!")
        break
    if remainingGuesses == 0:
        print("You lost")
        break

from abc import ABC, abstractmethod
from itertools import cycle, product
from random import choice


class Algorithm(ABC):
    """
    Abstract class for algorithms
    """

    def __init__(self, lengthOfCode: int, colours: dict[int, str]):
        self._lengthOfCode = lengthOfCode
        self._colourOptions = list(colours.keys())

    @abstractmethod
    def getNextGuess(self, previousResponse: list[int] = None) -> list:
        """
        Gets the next guess according to the algorithm
        """
        raise NotImplementedError()



class Random(Algorithm):
    """
    Random algorithm
    """

    def __init__(self, lengthOfCode: int, colours: dict[int, str]):
        super().__init__(lengthOfCode, colours)

    def getNextGuess(self, previousResponse: list[int] = None) -> list:
        """
        Gets the next guess according to the algorithm
        """
        return [choice(self._colourOptions) for _ in range(self._lengthOfCode)]


class RandomConsistent(Algorithm):
    """
    Random algorithm that is consistent with the feedback it is given
    """

    def __init__(self, lengthOfCode: int, colours: dict[int, str]):
        super().__init__(lengthOfCode, colours)
        self._previousGuess = None
        # create a set S of all possible guesses
        self._S = set(product(self._colourOptions, repeat=lengthOfCode))

    def getNextGuess(self, previousResponse: list[int] = None) -> list[int]:
        """
        Gets the next guess according to the algorithm.
        """
        if self._previousGuess is None:
            self._previousGuess = self._genInitialGuess()
            return self._previousGuess
        elif len(self._S) == 1:
            for e in self._S:
                break
            return list(e)
        elif len(self._S) == 0:
            raise ValueError("No possible guesses")
        elif previousResponse is None:
            raise ValueError("previousResponse cannot be None")
        else:
            # remove from S all guesses that would not give the same response if the current guess was the code
            self._S.difference_update(
                self._getGuessesThatWouldNotGiveSameResponse(
                    self._previousGuess, previousResponse
                )
            )
            # call _genNextGuess to get the next guess
            self._previousGuess = self._genNextGuess()
            return self._previousGuess
    
    def _genInitialGuess(self) -> list[int]:
        """
        Calculates the initial guess
        """
        x = [i for i in self._colourOptions for _ in range(2)]
        y = cycle(x)
        guess = []
        for _ in range(self._lengthOfCode):
            guess.append(next(y))
        return guess
    
    def _genNextGuess(self) -> list[int]:
        """
        Returns a random guess from the remaining guesses
        """
        return list(choice(list(self._S)))
    
    def _getGuessesThatWouldNotGiveSameResponse(
        self, guess: list[int], previousResponse: list[int]
    ) -> set[tuple[int]]:
        """
        Returns a set of all guesses that would not give the same response as the previous guess
        """
        guessesThatWouldNotGiveSameResponse = set()
        for code in self._S:
            # turn the code tuple into a list
            lcode = list(code)
            response = self._getResponse(guess, lcode)
            if response != previousResponse:
                guessesThatWouldNotGiveSameResponse.add(code)
        return guessesThatWouldNotGiveSameResponse
    
    def _getResponse(self, guess: list[int], code: list[int]) -> list:
        """
        Returns a list of the result of the guess against the code
        """
        result = []
        tempCode = code.copy()
        tempGuess = guess.copy()
        for i in range(len(guess)):
            if code[i] == guess[i]:
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


class Knuths(RandomConsistent):
    """
    A class that implements the knuths algorithm for generating guesses.
    Inherits from RandomConsistent, as it uses the same algorithm for steps 2-5.
    Knuths algorithm for generating guesses:
        1. create a set C of all possible codes
        2. create a set S of all possible guesses
        3. play the next guess
        4. if the guess is correct, terminate
        5. otherwise remove from S all guesses that would not give the same response if the current guess was the code
        6. calculate the next guess using minimax -> choose the guess that has the least worse response score
        7. repeat from step 3
    """

    def __init__(self, lengthOfCode: int, colours: dict[int, str]):
        super().__init__(lengthOfCode, colours)
        # set S from the superclass
        # create a set C of all possible codes
        self.__C = frozenset(self._S)

    def _genNextGuess(self) -> list[int]:
        """
        Calculates the next guess using minimax.
        Chooses the guess that has the best worst case scenario.
        """
        bestScore = -1
        possibleGuesses = set()
        for guess in self.__C:
            score = self.__calcScore(list(guess))
            if score[1] > bestScore:
                bestScore = score[1]
                possibleGuesses = {score}
            elif score[1] == bestScore:
                possibleGuesses.add(score)
        guesses = []
        for guess, _ in possibleGuesses:
            guesses.append(guess)
        guesses.sort()
        for guess in guesses:
            if guess in self._S:
                return list(guess)
        return list(guesses[0])

    def __calcScore(self, guess: list[int]) -> tuple[tuple[int], int]:
        """
        Calculates the score of a guess and returns a tuple of the guess and the score.
        The score is defined as the best worst case scenario.
        The minimum number of guesses that must be eliminated if making this guess.
        """
        minNumber = 999999999
        for response in self.__genPossibleResponses(guess):
            num = len(self._S) - len(
                self._S.difference(
                    self._getGuessesThatWouldNotGiveSameResponse(guess, list(response))
                )
            )
            if num < minNumber:
                minNumber = num
        return (tuple(guess), minNumber)

    def __genPossibleResponses(self, guess: list[int]) -> set[tuple[int]]:
        """
        Returns a set of all possible responses to a guess.
        """
        possibleResponses = set()
        for code in self._S:
            possibleResponses.add(tuple(self._getResponse(guess, list(code))))
        return possibleResponses

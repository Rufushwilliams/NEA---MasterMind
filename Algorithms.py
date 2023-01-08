from abc import ABC, abstractmethod
from itertools import permutations, product
from random import choice, sample
from typing import Generator, Iterable


class Algorithm(ABC):
    """
    Abstract class for algorithms
    """

    def __init__(self, lengthOfCode: int, colourNum: int, duplicatesAllowed: bool):
        self._lengthOfCode = lengthOfCode
        self._colourOptions = [i for i in range(1, colourNum + 1)]
        self._duplicatesAllowed = duplicatesAllowed

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

    def __init__(self, lengthOfCode: int, colourNum: int, duplicatesAllowed: bool):
        super().__init__(lengthOfCode, colourNum, duplicatesAllowed)

    def getNextGuess(self, previousResponse: list[int] = None) -> list:
        """
        Gets the next guess according to the algorithm
        """
        if self._duplicatesAllowed:
            return [choice(self._colourOptions) for _ in range(self._lengthOfCode)]
        return sample(self._colourOptions, self._lengthOfCode)


class RandomConsistent(Algorithm):
    """
    Random algorithm that is consistent with the feedback it is given
    """

    def __init__(self, lengthOfCode: int, colourNum: int, duplicatesAllowed: bool):
        super().__init__(lengthOfCode, colourNum, duplicatesAllowed)
        self._previousGuess = None
        # create a set S of all possible guesses
        if self._duplicatesAllowed:
            self._S = set(product(self._colourOptions, repeat=lengthOfCode))
        else:
            self._S = set(permutations(self._colourOptions, r=lengthOfCode))

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
        if self._duplicatesAllowed:
            x = [i for i in self._colourOptions for _ in range(2)]
        else:
            x = self._colourOptions.copy()
        y = self._cycle(x)
        guess = []
        for _ in range(self._lengthOfCode):
            guess.append(next(y))
        return guess

    def _cycle(self, iterable: Iterable) -> Generator:
        """
        Takes an iterable and returns a generator that repeatedly cycles through it.
        """
        saved = []
        for element in iterable:
            yield element
            saved.append(element)
        while saved:
            for element in saved:
                yield element

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

    def __init__(self, lengthOfCode: int, colourNum: int, duplicatesAllowed: bool):
        super().__init__(lengthOfCode, colourNum, duplicatesAllowed)
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
        guesses = self._mergeSort(guesses)
        for guess in guesses:
            if guess in self._S:
                return list(guess)
        return list(guesses[0])

    def _mergeSort(self, l: list) -> list:
        """
        A function that sorts a list using the mergesort algorithm.
        """
        ############################
        # GROUP A SKILL: MERGESORT #
        ############################
        # basis case
        if len(l) == 1:
            return l
        # find the middle of the list
        midPoint = len(l) // 2
        # split the list into two halves
        lHalf = l[:midPoint]
        rHalf = l[midPoint:]
        # recursively sort the two halves
        lHalf = self._mergeSort(lHalf)
        rHalf = self._mergeSort(rHalf)
        # merge the two halves
        newList = []
        while len(lHalf) > 0 and len(rHalf) > 0:
            if lHalf[0] < rHalf[0]:
                newList.append(lHalf.pop(0))
            else:
                newList.append(rHalf.pop(0))
        # add the remaining elements to the list
        if len(lHalf) > 0:
            newList += lHalf
        if len(rHalf) > 0:
            newList += rHalf
        return newList

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

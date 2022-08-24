from __future__ import annotations
from abc import ABC, abstractmethod
from itertools import cycle, product
from Board import Board


class Player(ABC):
    """
    Basic player class
    """

    def __init__(self, name: str):
        self._name = name.capitalize()

    def getName(self) -> str:
        return self._name

    @abstractmethod
    def getMove(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    @abstractmethod
    def getCode(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players code.
        """
        raise NotImplementedError()

    def displayBoard(self, board: Board, code: list = None):
        """
        Displays the board to the player.
        """
        pass

    def displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round.
        """
        pass

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner of the game.
        """
        pass


class Computer(Player):
    """
    Computer class that inherits from the Player class
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.__board = None
        self.__algorithm = None

    def __genAlgorithm(self, length: int, coloursAllowed: dict[int, str]):
        """
        Generates an instance of the algorithm for the AI to use.
        """
        self.__algorithm = knuthsAlgorithm(length, coloursAllowed)

    def getMove(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players next guess.
        """
        if self.__algorithm == None:
            self.__genAlgorithm(length, coloursAllowed)
        return self.__algorithm.getNextGuess(self.__getPreviousResponse())

    def getCode(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players code.
        """
        pass

    def displayBoard(self, board: Board, code: list = None):
        """
        Saves the board.
        """
        self.__board = board

    def displayRoundWinner(self, winner: Player):
        """
        Clears the saved board and algorithm.
        """
        self.__board = None
        self.__algorithm = None

    def __getPreviousResponse(self) -> list:
        """
        Returns the previous response from the board. If there is no board, it returns None.
        """
        if self.__board:
            return self.__board.getResults()[-1]
        return None


class knuthsAlgorithm:
    """
    A class that implements the knuths algorithm for generating guesses.
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
        self.__previousGuess = None
        self.__lengthOfCode = lengthOfCode
        self.__colourOptions = list(colours.keys())
        # create a set S of all possible guesses
        self.__S = set(product(self.__colourOptions, repeat=lengthOfCode))
        # create a set C of all possible codes
        self.__C = frozenset(self.__S)

    def getNextGuess(self, previousResponse: list[int] = None) -> list[int]:
        """
        Gets the next guess using the knuths algorithm.
        """
        if self.__previousGuess is None:
            self.__previousGuess = self.__genInitialGuess()
            return self.__previousGuess
        elif len(self.__S) == 1:
            for e in self.__S:
                break
            return list(e)
        elif len(self.__S) == 0:
            raise ValueError("No possible guesses")
        elif previousResponse is None:
            raise ValueError("previousResponse cannot be None")
        else:
            # remove from S all guesses that would not give the same response if the current guess was the code
            self.__S.difference_update(
                self.__getGuessesThatWouldNotGiveSameResponse(
                    self.__previousGuess, previousResponse
                )
            )
            # calculate the next guess using minimax -> choose the guess that has the least worse response score
            self.__previousGuess = self.__genNextGuess()
            return self.__previousGuess

    def __genInitialGuess(self) -> list[int]:
        """
        Calculates the initial guess
        """
        x = [i for i in self.__colourOptions for _ in range(2)]
        y = cycle(x)
        guess = []
        for _ in range(self.__lengthOfCode):
            guess.append(next(y))
        return guess

    def __getGuessesThatWouldNotGiveSameResponse(
        self, guess: list[int], previousResponse: list[int]
    ) -> set[tuple[int]]:
        """
        Returns a set of all guesses that would not give the same response as the previous guess
        """
        guessesThatWouldNotGiveSameResponse = set()
        for code in self.__S:
            # turn the code tuple into a list
            lcode = list(code)
            response = self.__getResponse(guess, lcode)
            if response != previousResponse:
                guessesThatWouldNotGiveSameResponse.add(code)
        return guessesThatWouldNotGiveSameResponse

    def __getResponse(self, guess: list[int], code: list[int]) -> list:
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

    def __genNextGuess(self) -> list[int]:
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
            if guess in self.__S:
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
            num = len(self.__S) - len(
                self.__S.difference(
                    self.__getGuessesThatWouldNotGiveSameResponse(guess, list(response))
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
        for code in self.__S:
            possibleResponses.add(tuple(self.__getResponse(guess, list(code))))
        return possibleResponses


class Human(Player, ABC):
    """
    Human class that inherits from the Player class
    """

    def __init__(self, name: str):
        super().__init__(name)
        pass


class LocalHuman(Human, ABC):
    """
    Local human class that inherits from the Human class
    UI is only needed for the local human class
    """

    def __init__(self, name: str):
        super().__init__(name)
        pass

    @abstractmethod
    def displayBoard(self, board: Board, code: list = None):
        """
        Displays the board to the ui
        """
        raise NotImplementedError()

    @abstractmethod
    def displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round to the ui.
        """
        raise NotImplementedError()

    @abstractmethod
    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        raise NotImplementedError()


class Terminal(LocalHuman):
    """
    Terminal class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game to the terminal
    """

    def __init__(self, name: str):
        super().__init__(name)
        pass

    def getMove(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players next guess.
        """
        colours = list(coloursAllowed.keys())
        print(f"{self._name}, please enter your guess of {length} digits long")
        while True:
            guess = input()
            if (
                guess.isdigit()
                and len(guess) == length
                and all(int(i) in colours for i in guess)
            ):
                break
            print("Please enter a valid guess")
        return [int(i) for i in guess]

    def getCode(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players code.
        """
        colours = list(coloursAllowed.keys())
        print(f"{self._name}, please enter your code of {length} digits long")
        while True:
            code = input()
            if (
                code.isdigit()
                and len(code) == length
                and all(int(i) in colours for i in code)
            ):
                break
            print("Please enter a valid code")
        return [int(i) for i in code]

    def displayBoard(self, board: Board, code: list = None):
        """
        Displays the board to the ui
        """
        print(board)
        if code:
            print(f"The code was {code}")
        print()

    def displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round to the ui.
        """
        print(f"{winner.getName()} wins this round!")

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        if winner is None:
            print("It's a draw!")
        else:
            print(f"Congrats!! The winner was {winner.getName()}")


class GUI(LocalHuman):
    """
    GUI class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game with a GUI
    """

    def __init__(self, name: str):
        super().__init__(name)
        pass


class NetworkingHuman(Human):
    """
    Networking human class that inherits from the Human class
    """

    def __init__(self, name: str):
        super().__init__(name)
        pass


class Statistics:
    """
    Statistics class that stores the statistics of a human player
    """

    def __init__(self):
        pass

    def getStats(self):
        pass

    def setStats(self):
        pass

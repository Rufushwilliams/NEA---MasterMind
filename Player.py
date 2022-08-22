from __future__ import annotations
from abc import ABC, abstractmethod
from itertools import product
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


class AI(Player):
    """
    AI class that inherits from the Player class
    """

    def __init__(self, name: str):
        super().__init__(name)
        pass

    def getMove(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players next guess.
        """
        from random import randint
        from time import sleep

        sleep(1)
        return [randint(1, list(coloursAllowed.keys())[-1]) for _ in range(length)]

        # TODO: Implement Knuth's algorithm

    def getCode(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players code.
        """
        pass


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
            return list(self.__S)[0]
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
        if self.__lengthOfCode == 4 and len(self.__colourOptions) == 6:
            return [1, 1, 2, 2]  # 1122 for a MM(4,6) game
        else:
            raise NotImplementedError()

    def __getGuessesThatWouldNotGiveSameResponse(
        self, guess: list[int], previousResponse: list[int]
    ) -> set[list[int]]:
        """
        Returns a set of all guesses that would not give the same response as the previous guess
        """
        guessesThatWouldNotGiveSameResponse = set()
        for code in self.__S:
            # turn the code tuple into a list
            code = list(code)
            response = self.__getResponse(guess, code)
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
        """
        raise NotImplementedError()


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

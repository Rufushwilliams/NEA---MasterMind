from __future__ import annotations
from abc import ABC, abstractmethod
from Board import Board
import Algorithms as alg


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
        self.__algorithm: alg.Algorithm = None

    def __genAlgorithm(self, length: int, coloursAllowed: dict[int, str]):
        """
        Generates an instance of the algorithm for the AI to use.
        """
        self.__algorithm = alg.Knuths(length, coloursAllowed)

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

    def getMove(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    def getCode(self, length: int, coloursAllowed: dict[int, str]) -> list:
        """
        Returns the players code.
        """
        raise NotImplementedError()

    def displayBoard(self, board: Board, code: list = None):
        """
        Displays the board to the ui
        """
        raise NotImplementedError()

    def displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round to the ui.
        """
        raise NotImplementedError()

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        raise NotImplementedError()


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

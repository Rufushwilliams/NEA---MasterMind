from __future__ import annotations
from abc import ABC, abstractmethod
from random import choice, sample
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
    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    @abstractmethod
    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
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

    def __init__(self, name: str, algorithmType: alg.Algorithm):
        super().__init__(name)
        self.__board = None
        self.__algorithmType = algorithmType
        self.__algorithm = None

    def __genAlgorithm(self, length: int, colourNum: int, duplicatesAllowed: bool):
        """
        Generates an instance of the algorithm for the AI to use.
        """
        self.__algorithm = self.__algorithmType(length, colourNum, duplicatesAllowed)

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        if self.__algorithm == None:
            self.__genAlgorithm(length, colourNum, duplicatesAllowed)
        return self.__algorithm.getNextGuess(self.__getPreviousResponse())

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
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

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        return self.__getPlayerInput(length, colourNum, duplicatesAllowed, "guess")

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players code.
        """
        return self.__getPlayerInput(length, colourNum, duplicatesAllowed, "code")

    def __getPlayerInput(
        self, length: int, colourNum: int, duplicatesAllowed: bool, message: str
    ) -> list[int]:
        """
        Returns the players input for either a guess or code.
        """
        colourOptions = [i for i in range(1, colourNum + 1)]
        if duplicatesAllowed:
            example = [choice(colourOptions) for _ in range(length)]
            x = ", each as many times as you want"
        else:
            example = sample(colourOptions, length)
            x = ", each only once"
        if colourNum >= 10:
            example = " ".join(str(i) for i in example)
            print(f"{self._name}, please enter your {message} of {length} numbers long")
            print(
                f"You may include the numbers 1 through {colourNum}{x}, seperated by spaces"
            )
            print(f"E.g. '{example}'")
            while True:
                guess = input()
                guess = guess.split(" ")
                if (
                    all(i.isdigit() for i in guess)
                    and len(guess) == length
                    and all(int(i) in colourOptions for i in guess)
                    and (duplicatesAllowed or len(set(guess)) == length)
                ):
                    break
                print(f"Please enter a valid {message}")
        else:
            example = "".join(str(i) for i in example)
            print(f"{self._name}, please enter your {message} of {length} numbers long")
            print(
                f"You may include the numbers 1 through {colourNum}{x}, with no seperation"
            )
            print(f"E.g. '{example}'")
            while True:
                guess = input()
                if (
                    guess.isdigit()
                    and len(guess) == length
                    and all(int(i) in colourOptions for i in guess)
                    and (duplicatesAllowed or len(set(guess)) == length)
                ):
                    break
                print(f"Please enter a valid {message}")
        return [int(i) for i in guess]

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

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
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

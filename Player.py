from __future__ import annotations
from abc import ABC, abstractmethod
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
    def getMove(self) -> list:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def getCode(self) -> list:
        """
        Returns the players code.
        """
        raise NotImplementedError()
    
    def displayBoard(self, board: Board):
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

    def getMove(self) -> list:
        """
        Returns the players next guess.
        """
        pass

    def getCode(self) -> list:
        """
        Returns the players code.
        """
        pass


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
    def displayBoard(self, board: Board):
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
            if guess.isdigit() and len(guess) == length and all(int(i) in colours for i in guess):
                break
            print("Please enter a valid guess")
        return [int(i) for i in guess]
    
    def getCode(self) -> list:
        """
        Returns the players code.
        """
        raise NotImplementedError()
        # print("Please enter your code")
        # while True:
        #     code = input()
        #     if len(code) == 4:
        #         break
        #     print("Please enter a valid code")
        # return list(code)

    def displayBoard(self, board: Board):
        """
        Displays the board to the ui
        """
        print(board)

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

from __future__ import annotations
from abc import ABC, abstractmethod
from random import choice, sample
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQtUI import boardWidget, SignalsGUI, loopSpinner
from Board import Board
import Algorithms as alg


class Player(ABC):
    """
    Basic player class
    """

    def __init__(self, playerName: str):
        self._playerName = playerName.capitalize()

    def getPlayerName(self) -> str:
        return self._playerName

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

    @abstractmethod
    def displayBoard(self, board: Board, code: list = None):
        """
        Displays the board to the player.
        """
        raise NotImplementedError()

    @abstractmethod
    def displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round.
        """
        raise NotImplementedError()

    @abstractmethod
    def displayWinner(self, winner: Player | None):
        """
        Displays the winner of the game.
        """
        raise NotImplementedError()

    @abstractmethod
    def displayRoundNumber(self, roundNumber: int):
        """
        Displays the round number.
        """
        raise NotImplementedError()


class Computer(Player):
    """
    Computer class that inherits from the Player class
    """

    def __init__(self, playerName: str, algorithmType: alg.Algorithm):
        super().__init__(playerName)
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
        colourOptions = [i for i in range(1, colourNum + 1)]
        if not duplicatesAllowed:
            return sample(colourOptions, length)
        return [choice(colourOptions) for _ in range(length)]

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

    def displayWinner(self, winner: Player | None):
        """
        The computer does not need to do anything when the game is over.
        """
        pass

    def displayRoundNumber(self, roundNumber: int):
        """
        The computer does not need to do anything when the round number changes.
        """
        pass

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

    def __init__(self, playerName: str):
        super().__init__(playerName)
        pass


class LocalHuman(Human, ABC):
    """
    Local human class that inherits from the Human class
    """

    def __init__(self, playerName: str):
        super().__init__(playerName)
        pass


class Terminal(LocalHuman):
    """
    Terminal class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game to the terminal
    """

    def __init__(self, playerName: str):
        super().__init__(playerName)
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
            print(
                f"{self._playerName}, please enter your {message} of {length} numbers long"
            )
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
            print(
                f"{self._playerName}, please enter your {message} of {length} numbers long"
            )
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
        print(f"{winner.getPlayerName()} wins this round!")

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        if winner is None:
            print("It's a draw!")
        else:
            print(f"Congrats!! The winner was {winner.getPlayerName()}")

    def displayRoundNumber(self, roundNumber: int):
        """
        Displays the round number to the ui
        """
        print("------------------------------")
        print("Round " + str(roundNumber))
        print("------------------------------")


class GUI(Player):
    """
    GUI class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game with a GUI
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.__colourMapping = {
            0: "#000000",
            1: "#FF0000",
            2: "#00FF00",
            3: "#0000FF",
            4: "#FFFF00",
            5: "#00FFFF",
            6: "#FF00FF",
            7: "#FFA500",
            8: "#6A0DAD",
        }
        self.__connectSignals()
        self.initUI()

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Calls the __getMove method and returns the result.
        Emits a signal to the GUI to get the players move.
        This is in order to allow the GUI to update and get player input.
        """
        loop = loopSpinner(self)
        return loop.result

    def __getMove(self, length: int, colourNum: int, duplicatesAllowed: bool):
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Calls the __getCode method and returns the result.
        Emits a signal to the GUI to get the players code.
        This is in order to allow the GUI to update and get player input.
        """
        loop = loopSpinner(self)
        return loop.result

    def __getCode(self, length: int, colourNum: int, duplicatesAllowed: bool):
        """
        Returns the players code.
        """
        raise NotImplementedError()

    def displayBoard(self, board: Board, code: list[int] = None):
        """
        Calls the __displayBoard method in the GUI.
        Emits a signal to the GUI to display the board.
        This is in order to draw the GUI on the main thread
        """
        self.signals.displayBoard.emit(board, code)

    def __displayBoard(self, board: Board, code: list[int] = None):
        """
        Displays the board to the ui
        """
        if any(i not in self.__colourMapping for i in board.getColours()):
            self.__colourMapping = self.__genColourMapping(board.getColours())
        guesses = board.getGuesses()
        results = board.getResults()
        lenOfGuess = board.getLenOfGuess()
        remainingGuesses = board.getRemainingGuesses()
        widget = boardWidget(
            guesses,
            results,
            lenOfGuess,
            remainingGuesses,
            self.__colourMapping,
            signal=self.signals.returnGuess,
        )
        self.__mainWindow.setCentralWidget(widget)

    def __genColourMapping(self, colours: list[int]):
        """
        Generates a mapping of colours to numbers
        """
        for i in colours:
            if i not in self.__colourMapping:
                colour = "#" + "".join([choice("0123456789ABCDEF") for _ in range(6)])
                if colour not in self.__colourMapping.values():
                    self.__colourMapping[i] = colour

    def displayRoundWinner(self, winner: Player):
        """
        Calls the __displayRoundWinner method in the GUI.
        Emits a signal to the GUI to display the round winner.
        This is in order to draw the GUI on the main thread
        """
        self.signals.displayRoundWinner.emit(winner)

    def __displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round to the ui
        """
        raise NotImplementedError()

    def displayWinner(self, winner: Player | None):
        """
        Calls the __displayWinner method in the GUI.
        Emits a signal to the GUI to display the winner.
        This is in order to draw the GUI on the main thread
        """
        self.signals.displayWinner.emit(winner)

    def __displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        raise NotImplementedError()

    def displayRoundNumber(self, roundNumber: int):
        """
        Displays the round number to the ui
        """
        return
        raise NotImplementedError()

    def __connectSignals(self):
        """
        Connects signals to the appropriate functions
        """
        self.signals = SignalsGUI()
        self.signals.getMove.connect(self.__getMove)
        self.signals.getCode.connect(self.__getCode)
        self.signals.displayBoard.connect(self.__displayBoard)
        self.signals.displayRoundWinner.connect(self.__displayRoundWinner)
        self.signals.displayWinner.connect(self.__displayWinner)

    def initUI(self):
        """
        Initialises the GUI
        """
        self.__mainWindow = qtw.QMainWindow()
        self.__mainWindow.setWindowTitle(f"Mastermind: {self._playerName}")
        self.__mainWidget = qtw.QWidget()
        self.__mainWidget.setFixedSize(qtc.QSize(800, 600))
        self.__mainWindow.setCentralWidget(self.__mainWidget)
        self.__mainWindow.showMaximized()


class NetworkingHuman(Human):
    """
    Networking human class that inherits from the Human class
    """

    def __init__(self, playerName: str):
        super().__init__(playerName)
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

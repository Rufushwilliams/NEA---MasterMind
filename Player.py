from __future__ import annotations
from abc import ABC, abstractmethod
from random import choice, sample
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQtPlayerUI import gameWidget, SignalsGUI, loopSpinner
from DataBaseManager import Statistics
from Board import Board
import Algorithms as alg


class Player(ABC):
    """
    Basic player class
    """

    def __init__(self, stats: Statistics):
        self._stats = stats

    def getUsername(self) -> str:
        return self._stats.username

    @abstractmethod
    def getMove(self, board: Board) -> list[int]:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    @abstractmethod
    def getCode(self, board: Board) -> list[int]:
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

    def __init__(self, stats: Statistics, algorithmType: alg.Algorithm):
        super().__init__(stats)
        self.__board = None
        self.__algorithmType = algorithmType
        self.__algorithm = None

    def __genAlgorithm(self, length: int, colourNum: int, duplicatesAllowed: bool):
        """
        Generates an instance of the algorithm for the AI to use.
        """
        self.__algorithm = self.__algorithmType(length, colourNum, duplicatesAllowed)

    def getMove(self, board: Board) -> list[int]:
        """
        Returns the players next guess.
        """
        length = board.getLenOfGuess()
        colourNum = len(board.getColours())
        duplicatesAllowed = board.getDuplicatesAllowed()
        if self.__algorithm == None:
            self.__genAlgorithm(length, colourNum, duplicatesAllowed)
        return self.__algorithm.getNextGuess(self.__getPreviousResponse())

    def getCode(self, board: Board) -> list[int]:
        """
        Returns the players code.
        """
        length = board.getLenOfGuess()
        colourOptions = board.getColours()
        duplicatesAllowed = board.getDuplicatesAllowed()
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

    def __init__(self, stats: Statistics):
        super().__init__(stats)
        pass


class LocalHuman(Human, ABC):
    """
    Local human class that inherits from the Human class
    """

    def __init__(self, stats: Statistics):
        super().__init__(stats)
        pass


class Terminal(LocalHuman):
    """
    Terminal class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game to the terminal
    """

    def __init__(self, stats: Statistics):
        super().__init__(stats)
        pass

    def getMove(self, board: Board) -> list[int]:
        """
        Returns the players next guess.
        """
        length = board.getLenOfGuess()
        colourNum = len(board.getColours())
        duplicatesAllowed = board.getDuplicatesAllowed()
        return self.__getPlayerInput(length, colourNum, duplicatesAllowed, "guess")

    def getCode(self, board: Board) -> list[int]:
        """
        Returns the players code.
        """
        length = board.getLenOfGuess()
        colourNum = len(board.getColours())
        duplicatesAllowed = board.getDuplicatesAllowed()
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
                f"{self.getUsername()}, please enter your {message} of {length} numbers long"
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
                f"{self.getUsername()}, please enter your {message} of {length} numbers long"
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
        print(f"{winner.getUsername()} wins this round!")

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        if winner is None:
            print("It's a draw!")
        else:
            print(f"Congrats!! The winner was {winner.getUsername()}")

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

    def __init__(self, stats: Statistics, popups: bool = True):
        super().__init__(stats)
        self.__popups = popups
        self.__colourMapping = {0: "#000000"}
        self.__roundNum = None
        self.initRound()
        self.__connectSignals()
        self.initUI()

    def initRound(self):
        self.__guessNum = 1
        self.__code = None

    def getMove(self, board: Board) -> list[int]:
        """
        Calls the __getMove method and returns the result.
        Emits a signal to the GUI to get the players move.
        This is in order to allow the GUI to update and get player input.
        """
        self.signals.getMove.emit(board)
        loop = loopSpinner(self)
        return loop.result

    def __getMove(self, board: Board):
        """
        Displays the board to the GUI, and makes the guess inputtable.
        """
        self.__displayBoard(
            board,
            guessEditable=True,
            message=f"Please enter guess number {self.__guessNum}",
        )
        self.__guessNum += 1

    def getCode(self, board: Board) -> list[int]:
        """
        Calls the __getCode method and returns the result.
        Emits a signal to the GUI to get the players code.
        This is in order to allow the GUI to update and get player input.
        """
        self.signals.getCode.emit(board)
        loop = loopSpinner(self)
        self.__code = loop.result
        return loop.result

    def __getCode(self, board: Board):
        """
        Displays the board to the GUI, and makes the code inputtable.
        """
        self.__displayBoard(board, codeEditable=True, message="Enter your code")

    def displayBoard(self, board: Board, code: list[int] = None):
        """
        Calls the __displayBoard method in the GUI.
        Emits a signal to the GUI to display the board.
        This is in order to draw the GUI on the main thread
        """
        self.signals.displayBoard.emit(board, code)

    def __displayBoard(
        self,
        board: Board,
        code: list[int] = None,
        codeEditable: bool = False,
        guessEditable: bool = False,
        message: str = None,
    ):
        """
        Displays the board to the ui
        """
        if any(i not in self.__colourMapping for i in board.getColours()):
            self.__genColourMapping(board.getColours())
        guesses = board.getGuesses()
        results = board.getResults()
        lenOfGuess = board.getLenOfGuess()
        remainingGuesses = board.getRemainingGuesses()
        duplicatesAllowed = board.getDuplicatesAllowed()
        self.widget = gameWidget(
            guesses,
            results,
            lenOfGuess,
            remainingGuesses,
            self.__colourMapping,
            code=code if code else self.__code,
            codeEditable=codeEditable,
            guessEditable=guessEditable,
            signal=self.signals.returnGuess,
            duplicatesAllowed=duplicatesAllowed,
            message=self.__getMessage(message)
            if message
            else self.__getMessage("Please wait..."),
        )
        self.__mainWindow.setCentralWidget(self.widget)

    def __getMessage(self, message: str):
        """
        Generates the message
        """
        return f"Round Number {str(self.__roundNum)}:\n{message}"

    def __genColourMapping(self, colours: list[int]):
        """
        Generates a mapping of colours to numbers
        """
        colourMapping = {
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
        for i in colours:
            if i not in self.__colourMapping:
                if i in colourMapping:
                    self.__colourMapping[i] = colourMapping[i]
                else:
                    colour = "#" + "".join(
                        [choice("0123456789ABCDEF") for _ in range(6)]
                    )
                    if colour not in self.__colourMapping.values():
                        self.__colourMapping[i] = colour

    def displayRoundWinner(self, winner: Player):
        """
        Calls the __displayRoundWinner method in the GUI.
        Emits a signal to the GUI to display the round winner.
        This is in order to draw the GUI on the main thread
        """
        self.signals.displayRoundWinner.emit(winner)
        if self.__popups:
            loopSpinner(self)

    def __displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round to the ui
        """
        self.initRound()
        if self.__popups:
            message = self.__getMessage(f"{winner.getUsername()} wins this round!")
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle("Round Winner")
            msgBox.setText(message)
            msgBox.setIcon(qtw.QMessageBox.Icon.Information)
            msgBox.exec()
            self.signals.returnGuess.emit([])

    def displayWinner(self, winner: Player | None):
        """
        Calls the __displayWinner method in the GUI.
        Emits a signal to the GUI to display the winner.
        This is in order to draw the GUI on the main thread
        """
        self.signals.displayWinner.emit(winner)
        if self.__popups:
            loopSpinner(self)

    def __displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        self.initRound()
        if self.__popups:
            message = (
                f"{winner.getUsername()} wins the game!" if winner else "It's a draw!"
            )
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle("Round Winner")
            msgBox.setText(message)
            msgBox.setIcon(qtw.QMessageBox.Icon.Information)
            msgBox.exec()
            self.signals.returnGuess.emit([])
        self.__mainWindow.hide()

    def displayRoundNumber(self, roundNumber: int):
        """
        Saves the round number in order to display it to the UI
        """
        self.__roundNum = roundNumber

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
        self.__mainWindow.setWindowTitle(f"Mastermind: {self.getUsername()}")
        self.__mainWidget = qtw.QWidget()
        self.__mainWidget.setFixedSize(qtc.QSize(800, 600))
        self.__mainWindow.setCentralWidget(self.__mainWidget)
        self.__mainWindow.showMaximized()


class NetworkingHuman(Human):
    """
    Networking human class that inherits from the Human class
    """

    def __init__(self, stats: Statistics):
        super().__init__(stats)
        pass

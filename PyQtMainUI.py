from dataclasses import fields
from enum import Enum
from ipaddress import ip_address
from random import choice, randint
from typing import Callable

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from DataBaseManager import Statistics


class LoginPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.usernameText = ""
        self.passwordText = ""
        self.setLayout(qtw.QVBoxLayout())
        self.usernameEnter = qtw.QLineEdit()
        self.usernameEnter.setFixedWidth(250)
        self.usernameEnter.setFixedHeight(50)
        self.usernameEnter.setPlaceholderText("Username")
        self.usernameEnter.setFont(qtg.QFont("Times", 20))
        self.usernameEnter.textChanged.connect(
            lambda t=self.usernameEnter.text(): self.updateUsernameText(t)
        )
        self.layout().addWidget(self.usernameEnter)
        self.passwordEnter = qtw.QLineEdit()
        self.passwordEnter.setFixedWidth(250)
        self.passwordEnter.setFixedHeight(50)
        self.passwordEnter.setPlaceholderText("Password")
        self.passwordEnter.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.passwordEnter.setFont(qtg.QFont("Times", 20))
        self.passwordEnter.textChanged.connect(
            lambda t=self.passwordEnter.text(): self.updatePasswordText(t)
        )
        self.layout().addWidget(self.passwordEnter)
        self.loginButton = qtw.QPushButton("Login")
        self.loginButton.setFixedWidth(250)
        self.loginButton.setFixedHeight(50)
        self.loginButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.loginButton)
        self.registerButton = qtw.QPushButton("Register")
        self.registerButton.setFixedWidth(250)
        self.registerButton.setFixedHeight(50)
        self.registerButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.registerButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(250)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))

    def showLoginError(self):
        error = qtw.QMessageBox()
        error.setIcon(qtw.QMessageBox.Icon.Critical)
        error.setText("Incorrect username or password")
        error.setWindowTitle("Error")
        error.exec()
        self.passwordEnter.clear()

    def showLoginSuccess(self):
        success = qtw.QMessageBox()
        success.setIcon(qtw.QMessageBox.Icon.Information)
        success.setText("Logged in!")
        success.setWindowTitle("Success")
        success.exec()
        self.usernameEnter.clear()
        self.passwordEnter.clear()

    def showRegisterError(self):
        error = qtw.QMessageBox()
        error.setIcon(qtw.QMessageBox.Icon.Critical)
        error.setText("Username already taken")
        error.setWindowTitle("Error")
        error.exec()
        self.usernameEnter.clear()
        self.passwordEnter.clear()

    def showRegisterSuccess(self):
        success = qtw.QMessageBox()
        success.setIcon(qtw.QMessageBox.Icon.Information)
        success.setText("Registered!")
        success.setWindowTitle("Success")
        success.exec()
        self.usernameEnter.clear()
        self.passwordEnter.clear()

    def updateUsernameText(self, text: str):
        self.usernameText = text

    def getUsername(self) -> str:
        return self.usernameText

    def getPassword(self) -> str:
        return self.passwordText

    def showBackButton(self):
        self.layout().addWidget(self.backButton)

    def hideBackButton(self):
        self.layout().removeWidget(self.backButton)

    def updatePasswordText(self, text: str):
        self.passwordText = text

    def bindLoginButton(self, *args: Callable):
        try:
            while True:
                self.loginButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.loginButton.clicked.connect(func)

    def bindRegisterButton(self, *args: Callable):
        try:
            while True:
                self.registerButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.registerButton.clicked.connect(func)

    def bindBackButton(self, *args: Callable):
        try:
            while True:
                self.backButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.backButton.clicked.connect(func)


class OnlineMultiplayerPage(qtw.QWidget):
    def __init__(self, textForConfirmButton: str):
        super().__init__()
        self.hostText = ""
        self.portText = ""
        self.setLayout(qtw.QVBoxLayout())
        self.hostEnter = qtw.QLineEdit()
        self.hostEnter.setFixedWidth(250)
        self.hostEnter.setFixedHeight(50)
        self.hostEnter.setPlaceholderText("Host")
        self.hostEnter.setFont(qtg.QFont("Times", 20))
        self.hostEnter.textChanged.connect(
            lambda t=self.hostEnter.text(): self.__updateHostText(t)
        )
        self.layout().addWidget(self.hostEnter)
        self.portEnter = qtw.QLineEdit()
        self.portEnter.setFixedWidth(250)
        self.portEnter.setFixedHeight(50)
        self.portEnter.setPlaceholderText("Port")
        self.portEnter.setFont(qtg.QFont("Times", 20))
        self.portEnter.textChanged.connect(
            lambda t=self.portEnter.text(): self.__updatePortText(t)
        )
        self.layout().addWidget(self.portEnter)
        self.confirmButton = qtw.QPushButton(textForConfirmButton)
        self.confirmButton.setFixedWidth(250)
        self.confirmButton.setFixedHeight(50)
        self.confirmButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.confirmButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(250)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def __updateHostText(self, text: str):
        self.hostText = text

    def __updatePortText(self, text: str):
        self.portText = text

    def getHost(self) -> str:
        return self.hostText

    def getPort(self) -> str:
        return self.portText

    def checkHostAndPortFormat(self) -> bool:
        """
        Checks the format of the host and port
        """
        if not self.getPort().isdigit():
            return False
        try:
            ip_address(self.getHost())
            return True
        except ValueError:
            return False

    def runConfirmButton(self, *args: Callable):
        """
        Runs the commands correlated to the confirm button if the host and port are of a valid format.
        Otherwise, it shows an error message.
        """
        if self.checkHostAndPortFormat():
            for func in args:
                func()
        else:
            error = qtw.QMessageBox()
            error.setIcon(qtw.QMessageBox.Icon.Critical)
            error.setText("Invalid host or port")
            error.setWindowTitle("Error")
            error.exec()

    def bindConfirmButton(self, *args: Callable):
        try:
            while True:
                self.confirmButton.clicked.disconnect()
        except TypeError:
            pass
        self.confirmButton.clicked.connect(lambda: self.runConfirmButton(*args))

    def bindBackButton(self, *args: Callable):
        try:
            while True:
                self.backButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.backButton.clicked.connect(func)


class WelcomePage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        welcomeLabel = qtw.QLabel("Welcome to Mastermind!")
        welcomeLabel.setFont(qtg.QFont("Times", 30))
        self.layout().addWidget(welcomeLabel)
        self.rulesButton = qtw.QPushButton("Press to see the rules")
        self.rulesButton.setFixedWidth(300)
        self.rulesButton.setFixedHeight(50)
        self.rulesButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.rulesButton)
        self.leaderboardButton = qtw.QPushButton("View Leaderboard")
        self.leaderboardButton.setFixedWidth(300)
        self.leaderboardButton.setFixedHeight(50)
        self.leaderboardButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.leaderboardButton)
        self.startButton = qtw.QPushButton("Start Game")
        self.startButton.setFixedWidth(300)
        self.startButton.setFixedHeight(50)
        self.startButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.startButton)
        self.logoutButton = qtw.QPushButton("Logout")
        self.logoutButton.setFixedWidth(300)
        self.logoutButton.setFixedHeight(50)
        self.logoutButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.logoutButton)
        self.exitButton = qtw.QPushButton("Exit")
        self.exitButton.setFixedWidth(300)
        self.exitButton.setFixedHeight(50)
        self.exitButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.exitButton)

    def bindRulesButton(self, *args: Callable):
        try:
            while True:
                self.rulesButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.rulesButton.clicked.connect(func)

    def bindLeaderboardButton(self, *args: Callable):
        try:
            while True:
                self.leaderboardButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.leaderboardButton.clicked.connect(func)

    def bindStartButton(self, *args: Callable):
        try:
            while True:
                self.startButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.startButton.clicked.connect(func)

    def bindLogoutButton(self, *args: Callable):
        try:
            while True:
                self.logoutButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.logoutButton.clicked.connect(func)

    def bindExitButton(self, *args: Callable):
        try:
            while True:
                self.exitButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.exitButton.clicked.connect(func)


class RulesPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        rulesLabel = qtw.QLabel("Rules")
        rulesLabel.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(rulesLabel)
        rulesBrowser = qtw.QTextBrowser()
        rulesText = """
        Mastermind is a code-breaking game for two players.
        These rules will describe the default settings for the game.

        The players take it in turns to guess the other player's secret code.
        The code is a sequence of four colours, chosen from six colours.
        The code may contain repeated colours.
        The player has six guesses to guess the code.
        After each guess, you will get feedback.
        This feedback tells you how many colours you have guessed correctly,
        and how many of those colours are in the correct place.
        It comes in the form of red and white pegs.
        A red peg means that you have guessed a colour correctly and it is in the correct place.
        A white peg means that you have guessed a colour correctly, but it is in the wrong place.
        The result pegs do not correspond to any peg from the guess in particular,
        but rather just the number of correct colours and correct positions.

        Once you have guessed the code, or you have run out of guesses, the round is over.
        The code guesser wins the round if they guess the code correctly.
        The code maker wins the round if the code guesser runs out of guesses.
        The code maker will then become the code guesser, and vice versa.
        The game is best of three rounds.

        Good luck!
        """
        rulesBrowser.append(rulesText)
        rulesBrowser.setFont(qtg.QFont("Times", 12))
        self.layout().addWidget(rulesBrowser)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def bindBackButton(self, *args: Callable):
        try:
            while True:
                self.backButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.backButton.clicked.connect(func)


class ModePage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        modeLabel = qtw.QLabel("Choose a mode")
        modeLabel.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(modeLabel)
        self.singleplayerButton = qtw.QPushButton("Singleplayer")
        self.singleplayerButton.setFixedWidth(300)
        self.singleplayerButton.setFixedHeight(50)
        self.singleplayerButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.singleplayerButton)
        self.localMultiplayerButton = qtw.QPushButton("Local Multiplayer")
        self.localMultiplayerButton.setFixedWidth(300)
        self.localMultiplayerButton.setFixedHeight(50)
        self.localMultiplayerButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.localMultiplayerButton)
        self.hostOnlineMultiplayerButton = qtw.QPushButton("Host Online Multiplayer")
        self.hostOnlineMultiplayerButton.setFixedWidth(300)
        self.hostOnlineMultiplayerButton.setFixedHeight(50)
        self.hostOnlineMultiplayerButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.hostOnlineMultiplayerButton)
        self.joinOnlineMultiplayerButton = qtw.QPushButton("Join Online Multiplayer")
        self.joinOnlineMultiplayerButton.setFixedWidth(300)
        self.joinOnlineMultiplayerButton.setFixedHeight(50)
        self.joinOnlineMultiplayerButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.joinOnlineMultiplayerButton)
        self.timedButton = qtw.QPushButton("Timed Mode")
        self.timedButton.setFixedWidth(300)
        self.timedButton.setFixedHeight(50)
        self.timedButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.timedButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def bindSingleplayerButton(self, *args: Callable):
        try:
            while True:
                self.singleplayerButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.singleplayerButton.clicked.connect(func)

    def bindLocalMultiplayerButton(self, *args: Callable):
        try:
            while True:
                self.localMultiplayerButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.localMultiplayerButton.clicked.connect(func)

    def bindHostOnlineMultiplayerButton(self, *args: Callable):
        try:
            while True:
                self.hostOnlineMultiplayerButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.hostOnlineMultiplayerButton.clicked.connect(func)

    def bindJoinOnlineMultiplayerButton(self, *args: Callable):
        try:
            while True:
                self.joinOnlineMultiplayerButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.joinOnlineMultiplayerButton.clicked.connect(func)

    def bindTimedButton(self, *args: Callable):
        try:
            while True:
                self.timedButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.timedButton.clicked.connect(func)

    def bindBackButton(self, *args: Callable):
        try:
            while True:
                self.backButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.backButton.clicked.connect(func)


class ReadyPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.startButton = qtw.QPushButton("Start Game")
        self.startButton.setFixedWidth(300)
        self.startButton.setFixedHeight(50)
        self.startButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.startButton)
        self.advancedSetupButton = qtw.QPushButton("Advanced Setup")
        self.advancedSetupButton.setFixedWidth(300)
        self.advancedSetupButton.setFixedHeight(50)
        self.advancedSetupButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.advancedSetupButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def bindStartButton(self, *args: Callable):
        try:
            while True:
                self.startButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.startButton.clicked.connect(func)

    def bindAdvancedSetupButton(self, *args: Callable):
        try:
            while True:
                self.advancedSetupButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.advancedSetupButton.clicked.connect(func)

    def bindBackButton(self, *args: Callable):
        try:
            while True:
                self.backButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.backButton.clicked.connect(func)


class LeaderBoardPage(qtw.QWidget):
    """
    A page that displays the leaderboard.
    The leaderboard should be passed in as a list of Statistics objects.
    These objects are in the order of display.
    The logged in player's stats are displayed at the top.
    The logged in player's statistics object should be passed in along with their position.
    """

    def __init__(self, leaderBoard: list[Statistics], player: tuple[Statistics, int]):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.layout().setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        txt = qtw.QLabel("Leaderboard")
        txt.setFont(qtg.QFont("Times", 36))
        self.layout().addWidget(txt)
        self.leaderBoard = LeaderBoard(leaderBoard, player)
        self.layout().addWidget(scrollArea(self.leaderBoard))
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def updateLeaderBoard(
        self, leaderBoard: list[Statistics], player: tuple[Statistics, int]
    ):
        self.leaderBoard.updateLeaderBoard(leaderBoard, player)

    def bindBackButton(self, *args: Callable):
        try:
            while True:
                self.backButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.backButton.clicked.connect(func)


class LeaderBoardTop(qtw.QWidget):
    """
    A widget that displays the top of the leaderboard.
    """

    def __init__(self, fieldNames: list[str], parse: bool = False):
        super().__init__()
        self.setLayout(qtw.QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().addWidget(LeaderBoardField("Position"))
        for field in fieldNames:
            fieldName = field
            if parse:
                fieldName = ""
                for char in field:
                    if char.isupper():
                        fieldName += " "
                    fieldName += char
                fieldName = fieldName.title()
            self.layout().addWidget(LeaderBoardField(fieldName))
        self.setFixedSize(self.sizeHint())


class LeaderBoardEntry(qtw.QWidget):
    """
    A widget that displays a single entry on the leaderboard.
    """

    def __init__(
        self, player: Statistics, position: int | str, highlight: bool = False
    ):
        super().__init__()
        self.setLayout(qtw.QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().addWidget(LeaderBoardField(f"{position}"))
        for field in fields(player):
            self.layout().addWidget(LeaderBoardField(f"{getattr(player, field.name)}"))
        if highlight:
            self.setStyleSheet("background-color: #00ff00;")
        self.setFixedSize(self.sizeHint())


class LeaderBoardField(qtw.QLabel):
    """
    A field on the leaderboard.
    """

    def __init__(self, value: str):
        super().__init__(f"{value}")
        self.setAlignment(
            qtc.Qt.AlignmentFlag.AlignHCenter | qtc.Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("border: 1px solid; padding: 5px; margin: 0px;")
        self.setFont(qtg.QFont("Arial", 14, qtg.QFont.Weight.Bold))
        self.setFixedSize(150, 50)


class LeaderBoard(qtw.QWidget):
    """
    A widget that displays the leaderboard.
    players should be a list of the Statistics objects of the players.
    It should be in the correct order.
    The current player can be passed in as a tuple of the Statistics object and their position.
    This will highlight their entry.
    """

    def __init__(
        self, players: list[Statistics], currPlayer: tuple[Statistics, int] = None
    ):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.layout().setSpacing(0)
        self.setLeaderBoard(players, currPlayer)

    def setLeaderBoard(
        self, players: list[Statistics], currPlayer: tuple[Statistics, int] = None
    ):
        self.layout().addWidget(
            LeaderBoardTop([field.name for field in fields(players[0])], True)
        )
        for i, player in enumerate(players):
            if currPlayer and currPlayer[0].username == player.username:
                currPlayer = None
                self.layout().addWidget(LeaderBoardEntry(player, i + 1, True))
            else:
                self.layout().addWidget(LeaderBoardEntry(player, i + 1))
        if currPlayer:
            self.layout().addWidget(
                LeaderBoardEntry(currPlayer[0], currPlayer[1], True)
            )
        self.setFixedSize(self.sizeHint())

    def updateLeaderBoard(
        self, players: list[Statistics], currPlayer: tuple[Statistics, int] = None
    ):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.setLeaderBoard(players, currPlayer)


class sliderOptionWidget(qtw.QWidget):
    def __init__(
        self, variable: str, defaultValue: int, label: str, min: int = 1, max: int = 99
    ):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.variable = variable
        self.labelText = label
        self.defaultValue = defaultValue
        self.initSlider(min, max)
        self.initLabel()
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.slider)

    def initSlider(self, min: int, max: int):
        self.slider = qtw.QSlider()
        self.slider.setOrientation(qtc.Qt.Orientation.Horizontal)
        self.slider.setRange(min, max)
        self.slider.setValue(self.defaultValue)
        self.slider.valueChanged.connect(self.onSliderMove)

    def initLabel(self):
        self.label = qtw.QLabel(f"{self.labelText}: {self.defaultValue}")
        self.label.setFont(qtg.QFont("Times", 20))

    def onSliderMove(self):
        self.label.setText(f"{self.labelText}: {self.slider.value()}")

    def restoreDefaultValue(self):
        self.slider.setValue(self.defaultValue)

    def getValue(self):
        return self.slider.value()


class radioButtonOptionWidget(qtw.QWidget):
    def __init__(self, variable: str, defaultValue, options: list[tuple], label: str):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.variable = variable
        self.labelText = label
        self.defaultValue = defaultValue
        self.initLabel()
        self.initButtons(options)
        self.layout().addWidget(self.label)
        for button in self.buttons:
            self.layout().addWidget(button)
        self.restoreDefaultValue()

    def initLabel(self):
        self.label = qtw.QLabel(f"{self.labelText}: {self.defaultValue}")
        self.label.setFont(qtg.QFont("Times", 20))

    def initButtons(self, options: list[tuple]):
        self.buttons = []
        for value, label in options:
            button = qtw.QRadioButton(str(label))
            button.value = value
            button.setFont(qtg.QFont("Times", 20))
            button.toggled.connect(self.onButtonToggle)
            self.buttons.append(button)

    def onButtonToggle(self):
        for button in self.buttons:
            if button.isChecked():
                self.label.setText(f"{self.labelText}: {button.text()}")

    def restoreDefaultValue(self):
        for button in self.buttons:
            if button.value == self.defaultValue:
                button.setChecked(True)

    def getValue(self):
        for button in self.buttons:
            if button.isChecked():
                return button.value


class AdvancedSetupPage(qtw.QWidget):
    def __init__(
        self,
        codeLengthDefault: int = 4,
        guessesDefault: int = 6,
        duplicatesAllowedDefault: bool = True,
        coloursDefault: int = 6,
        numRoundsDefault: int = 3,
        algorithmTypes: dict = None,
        algorithmTypeDefault=None,
    ):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        advancedSetupLabel = qtw.QLabel("Advanced Setup")
        advancedSetupLabel.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(advancedSetupLabel)

        self.options = []
        codeLengthSlider = sliderOptionWidget(
            "length", codeLengthDefault, "Code Length", 1, 99
        )
        self.options.append(codeLengthSlider)
        self.layout().addWidget(codeLengthSlider)
        guessesSlider = sliderOptionWidget(
            "numGuesses", guessesDefault, "Guesses", 1, 99
        )
        self.options.append(guessesSlider)
        self.layout().addWidget(guessesSlider)
        duplicatesAllowedRadio = radioButtonOptionWidget(
            "duplicatesAllowed",
            duplicatesAllowedDefault,
            [(True, True), (False, False)],
            "Duplicates Allowed",
        )
        self.options.append(duplicatesAllowedRadio)
        self.layout().addWidget(duplicatesAllowedRadio)
        uniquePegsSlider = sliderOptionWidget(
            "colourNum", coloursDefault, "Unique Pegs", 1, 99
        )
        self.options.append(uniquePegsSlider)
        self.layout().addWidget(uniquePegsSlider)
        numRoundsSlider = sliderOptionWidget(
            "numRounds", numRoundsDefault, "Number of Rounds", 1, 99
        )
        self.options.append(numRoundsSlider)
        self.layout().addWidget(numRoundsSlider)
        algorithmTypeRadio = radioButtonOptionWidget(
            "computerAlgorithmType",
            algorithmTypeDefault,
            [(value, value.__name__) for _, value in algorithmTypes.items()],
            "Algorithm Type",
        )
        self.options.append(algorithmTypeRadio)
        self.layout().addWidget(algorithmTypeRadio)

        restoreDefaultsButton = qtw.QPushButton("Restore Defaults")
        restoreDefaultsButton.setFixedWidth(300)
        restoreDefaultsButton.setFixedHeight(50)
        restoreDefaultsButton.setFont(qtg.QFont("Times", 20))
        restoreDefaultsButton.clicked.connect(lambda: self.restoreDefaultValues())
        self.layout().addWidget(restoreDefaultsButton)
        self.confirmButton = qtw.QPushButton("Confirm")
        self.confirmButton.setFixedWidth(300)
        self.confirmButton.setFixedHeight(50)
        self.confirmButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.confirmButton)

    def restoreDefaultValues(self):
        for option in self.options:
            option.restoreDefaultValue()

    def readOptionValues(self) -> dict[str, any]:
        values = {}
        for option in self.options:
            values[option.variable] = option.getValue()
        return values

    def bindConfirmButton(self, *args: Callable):
        try:
            while True:
                self.confirmButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.confirmButton.clicked.connect(func)


class circleWidget(qtw.QFrame):
    """
    A class that creates a circle widget with a given colour and radius.
    This widget can then be animated by the animation class.
    """

    def __init__(self, colour, radius: int):
        super().__init__()
        self.setFixedSize(radius, radius)
        self.setStyleSheet(
            f"border-radius: {self.width()//2}px; border: 1px solid black; background-color: {colour};"
        )


class animatedCircleWidget(circleWidget):
    """
    A class that creates a circle widget with a given colour and radius.
    It then animates the widget by moving it to a random position on the screen.
    """

    def __init__(
        self,
        colour,
        radius: int = 50,
        duration: int = 3000,
        moveFrom: qtc.QPoint = qtc.QPoint(0, 0),
        moveTo: qtc.QPoint = qtc.QPoint(100, 100),
    ):
        super().__init__(colour, radius)
        self.animation = qtc.QPropertyAnimation(self, b"pos")
        self.animation.setDuration(duration)
        self.setAnimationLocations(moveFrom, moveTo)
        self.animation.setEasingCurve(qtc.QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self.deleteLater)

    def setAnimationDuration(self, duration: int):
        self.animation.setDuration(duration)

    def setAnimationLocations(self, moveFrom: qtc.QPoint, moveTo: qtc.QPoint):
        self.animation.setStartValue(moveFrom)
        self.animation.setEndValue(moveTo)

    def startAnimation(self):
        self.animation.start()


class centreSpawningWidget(qtw.QFrame):
    """
    A class that creates a widget that spawns widgets in the centre of the screen
    """

    def __init__(self, num: int = 50):
        super().__init__()
        # get the screen size
        screenSize = qtw.QApplication.primaryScreen().size()
        self.setFixedSize(screenSize)
        for _ in range(num):
            self.createAnimatedColourWidget()

    def generateAnimatedColourWidget(self):
        """
        Creates a circle widget with a random colour and radius.
        The animation positions are not bound yet.
        """
        possibleColours = qtg.QColor().colorNames()
        colour = choice(possibleColours)
        r = randint(50, 130)
        cw = animatedCircleWidget(colour, r)
        cw.setParent(self)
        return cw

    def createAnimatedColourWidget(self):
        cw = self.generateAnimatedColourWidget()
        startPos = qtc.QPoint(
            self.width() // 2 - cw.width() // 2, self.height() // 2 - cw.height() // 2
        )
        cw.move(startPos)
        # choose a random position on the edge of the screen
        if choice([True, False]):
            # top or bottom
            x = randint(0, self.width())
            y = choice([-cw.height(), self.height()])
        else:
            # left or right
            x = choice([-cw.width(), self.width()])
            y = randint(0, self.height())
        endPos = qtc.QPoint(x, y)
        cw.setAnimationLocations(startPos, endPos)
        # randomly generate the duration
        duration = randint(3000, 10000)
        cw.setAnimationDuration(duration)
        # when the animation is finished, create a new widget
        cw.animation.finished.connect(self.createAnimatedColourWidget)
        # start the animation
        cw.lower()
        cw.show()
        cw.startAnimation()


class stackedWidget(qtw.QStackedWidget):
    """
    A class that creates a stacked widget.
    Its max size is the size of the screen multiplied by a given scale factor.
    """

    def __init__(self, scaleFactor: float = 0.7):
        super().__init__()
        # get the screen size
        screenSize = qtw.QApplication.primaryScreen().size()
        self.setFixedSize(screenSize * scaleFactor)
        # set the background colour without affecting the child widgets
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.ColorRole.Window, qtg.QColor("#f0f0f0"))
        self.setPalette(palette)


class mainWidget(qtw.QWidget):
    """
    A class that creates the main widget.
    It contains a stackedWidget and a centreSpawningWidget.
    """

    #################################################
    # GROUP A SKILL: COMPLEX USER DEFINED OOP MODEL #
    # GROUP A SKILL: DYNAMIC GENERATION OF OBJECTS  #
    #################################################

    def __init__(self):
        super().__init__()
        # get the screen size
        screenSize = qtw.QApplication.primaryScreen().size()
        self.setFixedSize(screenSize)
        # create the centre spawning widget
        self.centreSpawningWidget = centreSpawningWidget()
        self.centreSpawningWidget.setParent(self)
        self.centreSpawningWidget.show()
        # create the stacked widget
        self.stackedWidget = stackedWidget()
        self.stackedWidget.setParent(self)
        # move the stacked widget to the centre of the screen
        self.stackedWidget.move(
            self.width() // 2 - self.stackedWidget.width() // 2,
            self.height() // 2 - self.stackedWidget.height() // 2,
        )
        self.stackedWidget.show()


class scrollArea(qtw.QScrollArea):
    def __init__(self, widget: qtw.QWidget):
        super().__init__()
        self.setFrameShape(qtw.QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidget(widget)

    def wheelEvent(self, event: qtg.QWheelEvent):
        """
        Handles mouse wheel events.
        """
        # get the correct scrollbar depending on if the shift key is pressed
        scrollbar = self.verticalScrollBar()
        if event.modifiers() == qtc.Qt.KeyboardModifier.ShiftModifier:
            scrollbar = self.horizontalScrollBar()
        # get the direction of scroll
        action = qtw.QAbstractSlider.SliderAction.SliderSingleStepAdd
        if event.angleDelta().y() > 0:
            action = qtw.QAbstractSlider.SliderAction.SliderSingleStepSub
        # scroll the scrollbar
        scrollbar.triggerAction(action)
        scrollbar.triggerAction(action)
        scrollbar.triggerAction(action)


class gameModes(Enum):
    SINGLEPLAYER = 1
    LOCAL_MULTIPLAYER = 2
    HOST_ONLINE_MULTIPLAYER = 3
    JOIN_ONLINE_MULTIPLAYER = 4
    TIMED = 5

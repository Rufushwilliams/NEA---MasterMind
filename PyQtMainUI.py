from enum import Enum
from typing import Callable
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg


class LoginPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        usernameEnter = qtw.QLineEdit()
        usernameEnter.setFixedWidth(250)
        usernameEnter.setFixedHeight(50)
        usernameEnter.setPlaceholderText("Username")
        usernameEnter.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(usernameEnter)
        passwordEnter = qtw.QLineEdit()
        passwordEnter.setFixedWidth(250)
        passwordEnter.setFixedHeight(50)
        passwordEnter.setPlaceholderText("Password")
        passwordEnter.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        passwordEnter.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(passwordEnter)
        self.loginButton = qtw.QPushButton("Login")
        self.loginButton.setFixedWidth(250)
        self.loginButton.setFixedHeight(50)
        self.loginButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.loginButton)

    def bindLoginButton(self, func: Callable):
        self.loginButton.clicked.connect(func)


class WelcomePage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        welcomeLabel = qtw.QLabel("Welcome to Mastermind!")
        welcomeLabel.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(welcomeLabel)
        self.rulesButton = qtw.QPushButton("Press to see the rules")
        self.rulesButton.setFixedWidth(300)
        self.rulesButton.setFixedHeight(50)
        self.rulesButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.rulesButton)
        self.startButton = qtw.QPushButton("Start")
        self.startButton.setFixedWidth(300)
        self.startButton.setFixedHeight(50)
        self.startButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.startButton)

    def bindRulesButton(self, func: Callable):
        self.rulesButton.clicked.connect(func)

    def bindStartButton(self, func: Callable):
        self.startButton.clicked.connect(func)


class RulesPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        rulesLabel = qtw.QLabel("Rules")
        rulesLabel.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(rulesLabel)
        rulesBrowser = qtw.QTextBrowser()
        rulesText = "The rules are simple.\nThe computer will generate a code of four colours.\nYou will have six guesses to guess the code.\nThe computer will tell you how many colours you have guessed correctly,\nand how many of those colours are in the correct place.\nGood luck!"
        rulesBrowser.append(rulesText)
        rulesBrowser.setFont(qtg.QFont("Times", 12))
        self.layout().addWidget(rulesBrowser)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def bindBackButton(self, func: Callable):
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
        self.multiplayerButton = qtw.QPushButton("Multiplayer")
        self.multiplayerButton.setFixedWidth(300)
        self.multiplayerButton.setFixedHeight(50)
        self.multiplayerButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.multiplayerButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def bindSingleplayerButton(self, func: Callable):
        self.singleplayerButton.clicked.connect(func)

    def bindMultiplayerButton(self, func: Callable):
        self.multiplayerButton.clicked.connect(func)

    def bindBackButton(self, func: Callable):
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

    def bindStartButton(self, func: Callable):
        self.startButton.clicked.connect(func)

    def bindAdvancedSetupButton(self, func: Callable):
        self.advancedSetupButton.clicked.connect(func)

    def bindBackButton(self, func: Callable):
        self.backButton.clicked.connect(func)


class AdvancedSetupPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        advancedSetupLabel = qtw.QLabel("Advanced Setup")
        advancedSetupLabel.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(advancedSetupLabel)
        self.confirmButton = qtw.QPushButton("Confirm")
        self.confirmButton.setFixedWidth(300)
        self.confirmButton.setFixedHeight(50)
        self.confirmButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.confirmButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(300)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    def bindConfirmButton(self, func: Callable):
        self.confirmButton.clicked.connect(func)

    def bindBackButton(self, func: Callable):
        self.backButton.clicked.connect(func)


class gameModes(Enum):
    SINGLEPLAYER = 1
    MULTIPLAYER = 2


if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = qtw.mainUIWindow()
    app.exec()

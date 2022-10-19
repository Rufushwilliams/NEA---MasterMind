from enum import Enum
from typing import Callable
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


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


class JoinOnlineMultiplayerPage(qtw.QWidget):
    def __init__(self):
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
            lambda t=self.hostEnter.text(): self.updateUsernameText(t)
        )
        self.layout().addWidget(self.hostEnter)
        self.portEnter = qtw.QLineEdit()
        self.portEnter.setFixedWidth(250)
        self.portEnter.setFixedHeight(50)
        self.portEnter.setPlaceholderText("Port")
        self.portEnter.setFont(qtg.QFont("Times", 20))
        self.portEnter.textChanged.connect(
            lambda t=self.portEnter.text(): self.updatePasswordText(t)
        )
        self.layout().addWidget(self.portEnter)
        self.joinGameButton = qtw.QPushButton("Join Game")
        self.joinGameButton.setFixedWidth(250)
        self.joinGameButton.setFixedHeight(50)
        self.joinGameButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.joinGameButton)
        self.backButton = qtw.QPushButton("Back")
        self.backButton.setFixedWidth(250)
        self.backButton.setFixedHeight(50)
        self.backButton.setFont(qtg.QFont("Times", 20))
        self.layout().addWidget(self.backButton)

    # def showLoginError(self):
    #     error = qtw.QMessageBox()
    #     error.setIcon(qtw.QMessageBox.Icon.Critical)
    #     error.setText("Incorrect username or password")
    #     error.setWindowTitle("Error")
    #     error.exec()
    #     self.portEnter.clear()

    # def showLoginSuccess(self):
    #     success = qtw.QMessageBox()
    #     success.setIcon(qtw.QMessageBox.Icon.Information)
    #     success.setText("Logged in!")
    #     success.setWindowTitle("Success")
    #     success.exec()
    #     self.hostEnter.clear()
    #     self.portEnter.clear()

    # def showRegisterError(self):
    #     error = qtw.QMessageBox()
    #     error.setIcon(qtw.QMessageBox.Icon.Critical)
    #     error.setText("Username already taken")
    #     error.setWindowTitle("Error")
    #     error.exec()
    #     self.hostEnter.clear()
    #     self.portEnter.clear()

    # def showRegisterSuccess(self):
    #     success = qtw.QMessageBox()
    #     success.setIcon(qtw.QMessageBox.Icon.Information)
    #     success.setText("Registered!")
    #     success.setWindowTitle("Success")
    #     success.exec()
    #     self.hostEnter.clear()
    #     self.portEnter.clear()

    def updateHostText(self, text: str):
        self.hostText = text

    def updatePortText(self, text: str):
        self.portText = text

    def getHost(self) -> str:
        return self.hostText

    def getPort(self) -> str:
        return self.portText

    def bindJoinGameButton(self, *args: Callable):
        try:
            while True:
                self.joinGameButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.joinGameButton.clicked.connect(func)

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

    def bindRulesButton(self, *args: Callable):
        try:
            while True:
                self.rulesButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
            self.rulesButton.clicked.connect(func)

    def bindStartButton(self, *args: Callable):
        try:
            while True:
                self.startButton.clicked.disconnect()
        except TypeError:
            pass
        for func in args:
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


class gameModes(Enum):
    SINGLEPLAYER = 1
    LOCAL_MULTIPLAYER = 2
    HOST_ONLINE_MULTIPLAYER = 3
    JOIN_ONLINE_MULTIPLAYER = 4
    TIMED = 5

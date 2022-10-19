from typing import Callable, Type
from abc import ABC, abstractmethod
import threading
from PyQt6 import QtWidgets as qtw
from PyQt6.QtCore import QTimer
import PyQtMainUI as qtui
from DataBaseManager import dataBaseManager
from Game import Game
import Algorithms as alg
import Player as pl


class ResultThread(threading.Thread):
    """
    A thread that saves the result of the function it runs in thread.value
    """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.value = None

    def run(self):
        self.value = self._target(*self._args, **self._kwargs)


class UI(ABC):
    """
    Basic UI class used to display the game setup to the user
    """

    ALGORITHMTYPES = {
        1: alg.Random,
        2: alg.RandomConsistent,
        3: alg.Knuths,
    }

    DATABASE = "users.db"

    def __init__(
        self,
        length: int = 4,
        numGuesses: int = 6,
        numRounds: int = 3,
        duplicatesAllowed: bool = True,
        colourNum: int = 6,
        computerAlgorithmType: Type[alg.Algorithm] = alg.Knuths,
    ):
        self._length = length
        self._numGuesses = numGuesses
        self._numRounds = numRounds
        self._duplicatesAllowed = duplicatesAllowed
        self._colourNum = colourNum
        self._computerAlgorithmType = computerAlgorithmType
        self._dbm = dataBaseManager(self.DATABASE)

    @abstractmethod
    def run(self):
        """
        Runs the UI
        """
        raise NotImplementedError()


class GUI(UI):
    """
    GUI class that inherits from the UI class
    """

    def __init__(
        self,
        length: int = 4,
        numGuesses: int = 6,
        numRounds: int = 3,
        duplicatesAllowed: bool = True,
        colourNum: int = 6,
        computerAlgorithmType: Type[alg.Algorithm] = alg.Knuths,
    ):
        super().__init__(
            length,
            numGuesses,
            numRounds,
            duplicatesAllowed,
            colourNum,
            computerAlgorithmType,
        )
        self.p1Username = ""
        self.p2loggedin = False
        self.initUI()

    def run(self):
        """
        Runs the GUI
        """
        self.mainWindow.showMaximized()

    def initUI(self):
        # Create the main window
        self.mainWindow = qtw.QMainWindow()
        self.mainWidget = qtw.QStackedWidget()
        self.mainWindow.setCentralWidget(self.mainWidget)
        self.mainWindow.setWindowTitle("Mastermind")
        # Create all the pages
        self.loginPage = qtui.LoginPage()
        self.welcomePage = qtui.WelcomePage()
        self.rulesPage = qtui.RulesPage()
        self.modePage = qtui.ModePage()
        self.readyPage = qtui.ReadyPage()
        self.advancedSetupPage = qtui.AdvancedSetupPage(
            self._length,
            self._numGuesses,
            self._duplicatesAllowed,
            self._colourNum,
            self._numRounds,
            self.ALGORITHMTYPES,
            self._computerAlgorithmType,
        )
        self.joinOnlineMultiplayerPage = qtui.JoinOnlineMultiplayerPage()
        # Add all the pages to the main widget
        self.mainWidget.addWidget(self.loginPage)
        self.mainWidget.addWidget(self.welcomePage)
        self.mainWidget.addWidget(self.rulesPage)
        self.mainWidget.addWidget(self.modePage)
        self.mainWidget.addWidget(self.readyPage)
        self.mainWidget.addWidget(self.advancedSetupPage)
        self.mainWidget.addWidget(self.joinOnlineMultiplayerPage)

        # Setup the buttons on the pages
        self.__setupLoginPage(self.showWelcomePage)
        self.welcomePage.bindRulesButton(self.showRulesPage)
        self.welcomePage.bindStartButton(self.showModePage)
        self.rulesPage.bindBackButton(self.showWelcomePage)
        self.__setupModePage()
        self.readyPage.bindStartButton(self.initGame)
        self.readyPage.bindAdvancedSetupButton(self.showAdvancedSetupPage)
        self.readyPage.bindBackButton(self.showModePage)
        self.advancedSetupPage.bindConfirmButton(
            lambda: self.setValuesFromAdvanced(), lambda: self.showReadyPage()
        )
        self.joinOnlineMultiplayerPage.bindJoinGameButton(
            lambda: self.joinGame(
                host=self.joinOnlineMultiplayerPage.getHost(),
                port=self.joinOnlineMultiplayerPage.getPort(),
            )
        )
        self.joinOnlineMultiplayerPage.bindBackButton(self.showModePage)

    def __setupLoginPage(
        self,
        returnCommand: Callable,
        player1: bool = True,
        backButton: bool = False,
        backButtonCommand: Callable = None,
    ):
        self.loginPage.bindLoginButton(
            lambda e: self.tryLogin(
                self.loginPage.getUsername(),
                self.loginPage.getPassword(),
                returnCommand,
                player1,
            )
        )
        self.loginPage.bindRegisterButton(
            lambda e: self.tryRegister(
                self.loginPage.getUsername(),
                self.loginPage.getPassword(),
                returnCommand,
                player1,
            )
        )
        if backButton and backButtonCommand:
            self.loginPage.bindBackButton(backButtonCommand)
            self.loginPage.showBackButton()
        else:
            self.loginPage.hideBackButton()

    def __setupModePage(self):
        self.modePage.bindSingleplayerButton(
            lambda: self.setMode(qtui.gameModes.SINGLEPLAYER)
        )
        self.modePage.bindLocalMultiplayerButton(
            lambda: self.setMode(qtui.gameModes.LOCAL_MULTIPLAYER)
            if self.p2loggedin
            else (
                self.setMode(qtui.gameModes.LOCAL_MULTIPLAYER, show=False),
                self.__setupLoginPage(
                    self.showReadyPage,
                    player1=False,
                    backButton=True,
                    backButtonCommand=self.showModePage,
                ),
                self.showLoginPage(),
            )
        )
        # TODO: MAKE IT SO YOU CAN CHOOSE THE HOST AND PORT
        self.modePage.bindHostOnlineMultiplayerButton(
            lambda: self.setMode(qtui.gameModes.HOST_ONLINE_MULTIPLAYER),
        )
        self.modePage.bindJoinOnlineMultiplayerButton(
            lambda: self.setMode(qtui.gameModes.JOIN_ONLINE_MULTIPLAYER, show=False),
            lambda: self.showJoinOnlineMultiplayerPage(),
        )
        self.modePage.bindTimedButton(
            lambda: self.setMode(qtui.gameModes.TIMED, start=True)
        )
        self.modePage.bindBackButton(self.showWelcomePage)

    def showLoginPage(self):
        self.mainWidget.setCurrentWidget(self.loginPage)

    def showWelcomePage(self):
        self.mainWidget.setCurrentWidget(self.welcomePage)

    def showRulesPage(self):
        self.mainWidget.setCurrentWidget(self.rulesPage)

    def showModePage(self):
        self.mainWidget.setCurrentWidget(self.modePage)

    def showReadyPage(self):
        self.mainWidget.setCurrentWidget(self.readyPage)

    def showAdvancedSetupPage(self):
        self.mainWidget.setCurrentWidget(self.advancedSetupPage)

    def showJoinOnlineMultiplayerPage(self):
        self.mainWidget.setCurrentWidget(self.joinOnlineMultiplayerPage)

    def setMode(self, mode: qtui.gameModes, start: bool = False, show: bool = True):
        self._mode = mode
        if start:
            self.initGame()
        elif show:
            self.showReadyPage()

    def setValuesFromAdvanced(self):
        values = self.advancedSetupPage.readOptionValues()
        self._length = values["length"]
        self._numGuesses = values["numGuesses"]
        self._duplicatesAllowed = values["duplicatesAllowed"]
        self._colourNum = values["colourNum"]
        self._numRounds = values["numRounds"]
        self._computerAlgorithmType = values["computerAlgorithmType"]

    def tryLogin(  # TODO: Add a way to logout
        self,
        username: str,
        password: str,
        returnCommand: Callable,
        player1: bool = True,
    ):
        if username == self.p1Username:
            self.loginPage.showLoginError()
        elif username and self._dbm.login(username, password):
            stats = self._dbm.createStatsTable(username)
            if player1:
                self.p1Username = username
                self.player1 = pl.GUI(stats)
            else:
                self.player2 = pl.GUI(stats)
                self.p2loggedin = True
            self.loginPage.showLoginSuccess()
            returnCommand()
        else:
            self.loginPage.showLoginError()

    def tryRegister(
        self,
        username: str,
        password: str,
        returnCommand: Callable,
        player1: bool = True,
    ):
        if username and password and self._dbm.register(username, password):
            stats = self._dbm.createStatsTable(username)
            if player1:
                self.player1 = pl.GUI(stats)
            else:
                self.player2 = pl.GUI(stats)
            self.loginPage.showRegisterSuccess()
            returnCommand()
        else:
            self.loginPage.showRegisterError()

    def initGame(self):
        """
        Setup the game depending on the mode and other settings.
        Then call startGame.
        """
        length = self._length
        numGuesses = self._numGuesses
        duplicatesAllowed = self._duplicatesAllowed
        numRounds = self._numRounds
        colourNum = self._colourNum
        timed = False
        if self._mode == qtui.gameModes.SINGLEPLAYER:
            self.player2 = pl.Computer(
                self._dbm.createEmptyStatsTable("Computer"), self._computerAlgorithmType
            )
        elif self._mode == qtui.gameModes.LOCAL_MULTIPLAYER:
            pass
        elif self._mode == qtui.gameModes.HOST_ONLINE_MULTIPLAYER:
            # TODO: Make it so you can choose the host and port
            HOST = "127.0.0.1"
            PORT = 65432
            self.player2 = pl.serverPlayer(
                HOST, PORT, self._dbm.createEmptyStatsTable("Server")
            )
        elif self._mode == qtui.gameModes.JOIN_ONLINE_MULTIPLAYER:
            pass
        elif self._mode == qtui.gameModes.TIMED:
            self.player1.setPopups(False)
            self.player2 = pl.Computer(
                self._dbm.createEmptyStatsTable("Computer"), self._computerAlgorithmType
            )
            length = 4
            numGuesses = 6
            duplicatesAllowed = True
            numRounds = 1
            colourNum = 6
            timed = True
        else:
            raise ValueError("Invalid mode")
        game = Game(
            player1=self.player1,
            player2=self.player2,
            length=length,
            numGuesses=numGuesses,
            numRounds=numRounds,
            duplicatesAllowed=duplicatesAllowed,
            colourNum=colourNum,
        )
        self.showWelcomePage()
        self.startGame(game, timed)

    def joinGame(self, host, port):
        stats = self._dbm.createStatsTable(self.p1Username)
        p1 = pl.clientPlayer(host, port, stats)
        thread = threading.Thread(target=p1.playGame)
        thread.daemon = True
        thread.start()
        self.showWelcomePage()
        self.mainWindow.hide()

    def startGame(self, game, timed: bool = False):
        """
        Starts the game
        """
        self.mainWindow.hide()
        p1 = game.getPlayer1()
        p2 = game.getPlayer2()
        if type(p1) == pl.GUI:
            p1.show()
        if type(p2) == pl.GUI:
            p2.show()
        thread = ResultThread(target=game.run)
        thread.daemon = True
        self.timer = QTimer()
        self.timer.timeout.connect(
            lambda gameThread=thread, timed=timed: self.gameOver(gameThread, timed)
        )
        thread.start()
        self.timer.start(1000)

    def gameOver(self, gameThread, timed: bool = False):
        """
        Checks if the game thread is still running.
        If not, then it tidies up.
        Called with a timer on repeat.
        """
        if not gameThread.is_alive():
            self.timer.stop()
            self.mainWindow.show()
            if not gameThread.value:
                raise RuntimeError(
                    "Game thread returned None. Probably means the game crashed."
                )
            timeTaken, won = gameThread.value
            if timed:
                self.timedModeOver(timeTaken, won)
            if type(self.player1) == pl.GUI:
                self._dbm.saveStatsTable(self.player1.getStats())
            if type(self.player2) == pl.GUI:
                self._dbm.saveStatsTable(self.player2.getStats())

    def timedModeOver(self, timeTaken, won):
        if won:
            msg = f"You took {timeTaken} seconds to win!"
        else:
            msg = "You lost!"
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle("Timed Game Over")
        msgBox.setText(msg)
        msgBox.setIcon(qtw.QMessageBox.Icon.Information)
        msgBox.exec()


class Terminal(UI):
    """
    Terminal class that inherits from the UI class
    """

    def __init__(
        self,
        length: int = 4,
        numGuesses: int = 6,
        numRounds: int = 3,
        duplicatesAllowed: bool = True,
        colourNum: int = 6,
        computerAlgorithmType: Type[alg.Algorithm] = alg.Knuths,
    ):
        super().__init__(
            length,
            numGuesses,
            numRounds,
            duplicatesAllowed,
            colourNum,
            computerAlgorithmType,
        )

    def setup(self):
        """
        Sets up the game
        """
        print("-------------------------------------------------------")
        print("Please enter the following information to setup the game")
        print("-------------------------------------------------------")

        print("How long do you want the code to be? (default 4)")
        while True:
            codeLength = input()
            if codeLength.isdigit() and int(codeLength) > 0:
                break
            print("Please enter a valid number")
        self._length = int(codeLength)
        print("-------------------------------------------------------")
        print("How many guesses do you want to have? (default 6)")
        while True:
            guesses = input()
            if guesses.isdigit() and int(guesses) > 0:
                break
            print("Please enter a valid number")
        self._numGuesses = int(guesses)
        print("-------------------------------------------------------")
        print("Do you want to allow duplicates? (y/n) (default y)")
        while True:
            duplicates = input()
            if duplicates.lower() in ["y", "n"]:
                if duplicates.lower() == "y":
                    duplicates = True
                else:
                    duplicates = False
                break
            print("Please enter y or n")
        self._duplicatesAllowed = duplicates
        print("-------------------------------------------------------")
        print("How many unique pegs do you want? (default 6)")
        while True:
            colourNum = input()
            if (
                colourNum.isdigit()
                and int(colourNum) > 0
                and (self._duplicatesAllowed or int(colourNum) >= self._length)
            ):
                break
            print("Please enter a valid number")
        self._colourNum = int(colourNum)
        print("-------------------------------------------------------")
        print("How many rounds do you want to play? (default 3)")
        while True:
            rounds = input()
            if rounds.isdigit():
                break
            print("Please enter a valid number")
        self._numRounds = int(rounds)
        print("-------------------------------------------------------")
        print("What algorithm do you want the computer to use? (default Knuths)")
        for key, value in self.ALGORITHMTYPES.items():
            print(f"Enter {key} for {value.__name__}")
        while True:
            algorithm = input()
            if algorithm.isdigit() and int(algorithm) in self.ALGORITHMTYPES.keys():
                break
            print("Please enter a valid number")
        self._computerAlgorithmType = self.ALGORITHMTYPES[int(algorithm)]
        print("-------------------------------------------------------")
        print("Game setup complete")
        print("-------------------------------------------------------")

    def loginUser(self) -> pl.Player:
        """
        Asks the user to login and returns the player object for the user.
        """
        print("-------------------------------------------------------")
        print("Please login")
        print("-------------------------------------------------------")
        while True:
            username = input("Enter your username: ")
            if username:
                password = input("Enter your password: ")
                if self._dbm.login(username, password):
                    print("Login successful")
                    break
            print("Invalid username or password")
        stats = self._dbm.createStatsTable(username)
        return pl.Terminal(stats)

    def registerUser(self) -> pl.Player:
        """
        Registers a new user, and returns the player object for the user.
        """
        print("-------------------------------------------------------")
        print("Please register")
        print("-------------------------------------------------------")
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username and password and self._dbm.register(username, password):
                print("Registration successful")
                break
            print("Registration failed")
        stats = self._dbm.createStatsTable(username)
        return pl.Terminal(stats)

    def getPlayer(self, msg: str = None) -> pl.Player:
        """
        Asks the user if they want to login or register, and returns the player object for the user.
        """
        print("-------------------------------------------------------")
        if msg:
            print(msg)
        print("Do you want to login or register?")
        while True:
            choice = input("Enter l to login or r to register: ")
            if choice.lower() == "l":
                return self.loginUser()
            elif choice.lower() == "r":
                return self.registerUser()
            print("Please enter l or r")

    def run(self):
        """
        Runs the UI
        """
        while True:
            print("-------------------------------------------------------")
            print("Welcome to Mastermind")
            print("Enter 1 to play against a computer")
            print("Enter 2 to play against another human")
            print("Enter 3 to play timed mode")
            print("Enter 4 edit game settings")
            print("Enter 5 to exit")
            print("-------------------------------------------------------")
            choice = input("Enter your choice: ")
            if choice == "1":
                print("You have chosen to play against a computer")
                player1 = self.getPlayer("Hello Player 1!")
                player2 = pl.Computer(
                    self._dbm.createEmptyStatsTable("Computer"),
                    self._computerAlgorithmType,
                )
                game = Game(
                    player1,
                    player2,
                    self._length,
                    self._numGuesses,
                    self._numRounds,
                    self._duplicatesAllowed,
                    self._colourNum,
                )
                game.run()
                self._dbm.saveStatsTable(player1.getStats())
                continue
            elif choice == "2":
                print("You have chosen to play against another human")
                player1 = self.getPlayer("Hello Player 1!")
                player2 = self.getPlayer("Hello Player 2!")
                game = Game(
                    player1,
                    player2,
                    self._length,
                    self._numGuesses,
                    self._numRounds,
                    self._duplicatesAllowed,
                    self._colourNum,
                )
                game.run()
                self._dbm.saveStatsTable(player1.getStats())
                self._dbm.saveStatsTable(player2.getStats())
                continue
            elif choice == "3":
                print("You have chosen to play timed mode")
                player1 = self.getPlayer("Hello Player 1!")
                player2 = pl.Computer(
                    self._dbm.createEmptyStatsTable("Computer"),
                    self._computerAlgorithmType,
                )
                game = Game(player1, player2, 4, 6, 1, True, 6)
                timeTaken, win = game.run()
                print("-------------------------------------------------------")
                if win:
                    print(f"You have finished in {timeTaken} seconds")
                else:
                    print("You have lost")
                self._dbm.saveStatsTable(player1.getStats())
                continue
            elif choice == "4":
                self.setup()
                continue
            elif choice == "5":
                print("Exiting game...")
                quit(0)
            else:
                print("Invalid choice")
                continue

from typing import Type
from abc import ABC, abstractmethod
from time import time
from threading import Thread
from PyQt6 import QtWidgets as qtw
from Game import Game
import Algorithms as alg
import Player as pl


class UI(ABC):
    """
    Basic UI class used to display the game setup to the user
    """

    ALGORITHMTYPES = {
        1: alg.Random,
        2: alg.RandomConsistent,
        3: alg.Knuths,
    }

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

    def run(self):
        """
        Runs the GUI
        """
        app = qtw.QApplication([])
        self.mw = qtw.QMainWindow()
        print("Welcome to Mastermind!")
        player1 = pl.GUI("Player 1")
        player2 = pl.GUI("Player 2")
        game = Game(
            player1,
            player2,
            self._length,
            self._numGuesses,
            1,
            self._duplicatesAllowed,
            self._colourNum,
        )
        button = qtw.QPushButton("Click Me")
        button.clicked.connect(lambda: self.startGame(game))
        self.mw.setCentralWidget(button)
        self.mw.showMaximized()
        app.exec()
        raise NotImplementedError()

    def startGame(self, game):
        """
        Starts the game
        """
        self.mw.hide()
        thread = Thread(target=game.run)
        thread.start()


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
                name = input("Please enter your name: ")
                player1 = pl.GUI(name)
                player2 = pl.Computer("Computer", self._computerAlgorithmType)
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
                continue
            elif choice == "2":
                print("You have chosen to play against another human")
                name = input("Please enter the name of player 1: ")
                player1 = pl.Terminal(name)
                name = input("Please enter the name of player 2: ")
                player2 = pl.Terminal(name)
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
                continue
            elif choice == "3":
                print("You have chosen to play timed mode")
                name = input("Please enter your name: ")
                player1 = pl.Terminal(name)
                player2 = pl.Computer("Computer", self._computerAlgorithmType)
                game = Game(player1, player2, 4, 6, 1, self._duplicatesAllowed, 6)
                startTime = time()
                game.run()
                endTime = time()
                print("-------------------------------------------------------")
                print(f"You have finished in {endTime-startTime} seconds")
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

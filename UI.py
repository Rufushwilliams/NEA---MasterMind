from abc import ABC, abstractmethod
from time import time
from Game import Game
import Player


class UI(ABC):
    """
    Basic UI class used to display the game setup to the user
    """

    def __init__(
        self,
        length: int = 4,
        numGuesses: int = 6,
        numRounds: int = 1,
        duplicatesAllowed: bool = True,
    ):
        self._length = length
        self._numGuesses = numGuesses
        self._numRounds = numRounds
        self._duplicatesAllowed = duplicatesAllowed

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
        numRounds: int = 1,
        duplicatesAllowed: bool = False,
    ):
        super().__init__(length, numGuesses, numRounds, duplicatesAllowed)

    def run(self):
        """
        Runs the GUI
        """
        raise NotImplementedError()


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
    ):
        super().__init__(length, numGuesses, numRounds, duplicatesAllowed)

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
            if codeLength.isdigit():
                break
            print("Please enter a valid number")
        self._length = int(codeLength)
        print("-------------------------------------------------------")
        print("How many guesses do you want to have? (default 6)")
        while True:
            guesses = input()
            if guesses.isdigit():
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
        print("How many rounds do you want to play? (default 3)")
        while True:
            rounds = input()
            if rounds.isdigit():
                break
            print("Please enter a valid number")
        self._numRounds = int(rounds)
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
                player1 = Player.Terminal(name)
                player2 = Player.Computer("Computer")
                game = Game(
                    player1,
                    player2,
                    self._length,
                    self._numGuesses,
                    self._numRounds,
                    self._duplicatesAllowed,
                )
                game.run()
                continue
            elif choice == "2":
                print("You have chosen to play against another human")
                name = input("Please enter the name of player 1: ")
                player1 = Player.Terminal(name)
                name = input("Please enter the name of player 2: ")
                player2 = Player.Terminal(name)
                game = Game(
                    player1,
                    player2,
                    self._length,
                    self._numGuesses,
                    self._numRounds,
                    self._duplicatesAllowed,
                )
                game.run()
                continue
            elif choice == "3":
                print("You have chosen to play timed mode")
                name = input("Please enter your name: ")
                player1 = Player.Terminal(name)
                player2 = Player.Computer("Computer")
                game = Game(
                    player1,
                    player2,
                    self._length,
                    self._numGuesses,
                    1,
                    self._duplicatesAllowed,
                )
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

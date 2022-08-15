from abc import ABC, abstractmethod
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
        duplicatesAllowed: bool = False,
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
        duplicatesAllowed: bool = False,
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
        print("Do you want to allow duplicates? (y/n) (default n)")
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
            print("Enter 3 edit game settings")
            print("Enter 4 to exit")
            print("-------------------------------------------------------")
            choice = input("Enter your choice: ")
            match choice:
                case "1":
                    print("You have chosen to play against a computer")
                    name = input("Please enter your name: ")
                    player1 = Player.Terminal(name)
                    player2 = Player.AI("Computer")
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
                case "2":
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
                case "3":
                    self.setup()
                    continue
                case "4":
                    print("Exiting game...")
                    quit(0)
                case _:
                    print("Invalid choice")
                    continue

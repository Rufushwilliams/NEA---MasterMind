from __future__ import annotations


class Player:
    """
    Basic player class
    """

    def __init__(self, name: str):
        self.__name = name

    def getName(self) -> str:
        return self.__name

    def getMove(self) -> list:
        """
        Returns the players next guess.
        Abstract method
        """
        raise NotImplementedError()


class AI(Player):
    """
    AI class that inherits from the Player class
    """

    def __init__(self):
        super.__init__(self)
        raise NotImplementedError()


class Human(Player):
    """
    Human class that inherits from the Player class
    """

    def __init__(self):
        super.__init__(self)
        raise NotImplementedError()


class LocalHuman(Human):
    """
    Local human class that inherits from the Human class
    UI is only needed for the local human class
    """

    def __init__(self):
        super.__init__(self)
        raise NotImplementedError()

    def displayGuess(self, guess: list, result: list):
        """
        Displays the guess and result to the ui.
        Abstract method
        """
        raise NotImplementedError()
    
    def displayWinner(self, winner: Player):
        """
        Displays the winner to the ui
        Abstract method
        """
        raise NotImplementedError()


class Terminal(LocalHuman):
    """
    Terminal class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game to the terminal
    """

    def __init__(self):
        super.__init__(self)
        raise NotImplementedError()
    
    def getMove(self) -> list:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()
    
    def displayGuess(self, guess: list, result: list):
        """
        Displays the guess and result to the ui
        """
        print(f"You guessed {guess} and got {result}")
        #raise NotImplementedError()
    
    def displayWinner(self, winner: Player):
        """
        Displays the winner to the ui
        """
        print(f"Congrats!! The winner was {winner.getName()}")
        #raise NotImplementedError()


class GUI(LocalHuman):
    """
    GUI class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game with a GUI
    """

    def __init__(self):
        super.__init__(self)
        raise NotImplementedError()


class NetworkingHuman(Human):
    """
    Networking human class that inherits from the Human class
    """

    def __init__(self):
        super.__init__(self)
        raise NotImplementedError()


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

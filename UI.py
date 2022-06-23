from Game import Game


class UI:
    """
    Basic UI class
    """

    def __init__(self, game: Game):
        self._game = game

    def displayBoard(self):
        """
        Prints the board
        """
        raise NotImplementedError()


class GUI(UI):
    """
    GUI class that inherits from the UI class
    """

    def __init__(self, game):
        super.__init__(self, game)
        pass


class Terminal(UI):
    """
    Terminal class that inherits from the UI class
    """

    def __init__(self, game):
        super.__init__(self, game)
        pass

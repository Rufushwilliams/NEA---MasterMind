from __future__ import annotations
from abc import ABC, abstractmethod
from threading import Thread
from time import sleep
import tkinter as tk
import tkinter.messagebox as tkmb
from random import choice, sample
from Board import Board
import Algorithms as alg


class Player(ABC):
    """
    Basic player class
    """

    def __init__(self, playerName: str):
        self._playerName = playerName.capitalize()

    def getPlayerName(self) -> str:
        return self._playerName

    @abstractmethod
    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    @abstractmethod
    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
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


class Computer(Player):
    """
    Computer class that inherits from the Player class
    """

    def __init__(self, playerName: str, algorithmType: alg.Algorithm):
        super().__init__(playerName)
        self.__board = None
        self.__algorithmType = algorithmType
        self.__algorithm = None

    def __genAlgorithm(self, length: int, colourNum: int, duplicatesAllowed: bool):
        """
        Generates an instance of the algorithm for the AI to use.
        """
        self.__algorithm = self.__algorithmType(length, colourNum, duplicatesAllowed)

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        if self.__algorithm == None:
            self.__genAlgorithm(length, colourNum, duplicatesAllowed)
        return self.__algorithm.getNextGuess(self.__getPreviousResponse())

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players code.
        """
        colourOptions = [i for i in range(1, colourNum + 1)]
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

    def __init__(self, playerName: str):
        super().__init__(playerName)
        pass


class LocalHuman(Human, ABC):
    """
    Local human class that inherits from the Human class
    """

    def __init__(self, playerName: str):
        super().__init__(playerName)
        pass


class Terminal(LocalHuman):
    """
    Terminal class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game to the terminal
    """

    def __init__(self, playerName: str):
        super().__init__(playerName)
        pass

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        return self.__getPlayerInput(length, colourNum, duplicatesAllowed, "guess")

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players code.
        """
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
                f"{self._playerName}, please enter your {message} of {length} numbers long"
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
                f"{self._playerName}, please enter your {message} of {length} numbers long"
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
        print(f"{winner.getPlayerName()} wins this round!")

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        if winner is None:
            print("It's a draw!")
        else:
            print(f"Congrats!! The winner was {winner.getPlayerName()}")


class GUI(Player, Thread):
    """
    GUI class that inherits from the LocalHuman class
    This class is used as the LocalHuman class when displaying the game with a GUI
    A thread is created to run the GUI in the background
    """

    def __init__(self, name: str):
        super().__init__(name)
        Thread.__init__(self)
        self.__ready = False
        self.__colourPegMapping = None
        self.daemon = True
        self.start()
        # lock main thread until the GUI is ready
        while not self.__ready:
            sleep(0.1)

    def getMove(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players next guess.
        """
        raise NotImplementedError()

    def getCode(
        self, length: int, colourNum: int, duplicatesAllowed: bool
    ) -> list[int]:
        """
        Returns the players code.
        """
        raise NotImplementedError()

    def displayBoard(self, board: Board, code: list = None):
        """
        Displays the board to the ui
        """
        # get variables from board
        colours = board.getColours()
        if self.__colourPegMapping is None:
            self.__genColourPegMapping(colours)
        lenOfGuess = board.getLenOfGuess()
        guesses = board.getGuesses()
        results = board.getResults()
        remainingGuesses = board.getRemainingGuesses()
        # remove old board widget from root
        children = self.__root.winfo_children()
        for child in children:
            if child.winfo_name() == "board":
                child.destroy()
        # create the frame for the board
        frame = tk.Frame(self.__root, name="board")
        row = self.__drawRow(frame, [1] * lenOfGuess)
        resultBox = self.__drawResult(frame, lenOfGuess, [])
        xdistance = row.winfo_width() + resultBox.winfo_width()
        ydistance = row.winfo_height()
        frame.config(
            width=xdistance, height=ydistance * (len(guesses) + remainingGuesses)
        )
        # draw the already made guesses and results
        for i, (guess, result) in enumerate(zip(guesses, results)):
            c = tk.Canvas(frame, width=xdistance, height=ydistance)
            row = self.__drawRow(c, guess)
            row.create_text(25, 10, text=f"Guess {i+1}")
            resultBox = self.__drawResult(c, lenOfGuess, result)
            row.grid(row=0, column=0)
            resultBox.grid(row=0, column=1)
            c.pack(side=tk.BOTTOM)
        # draw the remaining guesses
        for i in range(remainingGuesses):
            c = tk.Canvas(frame, width=xdistance, height=ydistance)
            row = self.__drawRow(c, [0] * lenOfGuess)
            row.create_text(25, 10, text=f"Guess {len(guesses)+i+1}")
            resultBox = self.__drawResult(c, lenOfGuess, [])
            row.grid(row=0, column=0)
            resultBox.grid(row=0, column=1)
            c.pack(side=tk.BOTTOM)
        # draw the code
        if code:
            c = tk.Canvas(frame, width=xdistance, height=ydistance)
            codeCanvas = self.__drawRow(c, code)
            codeCanvas.create_text(25, 10, text="Code:")
            codeCanvas.pack(side=tk.TOP)
            c.pack(side=tk.BOTTOM)
        frame.pack(side=tk.RIGHT)

    def __genColourPegMapping(self, colours: list[int]):
        """
        Generates a mapping of colours to numbers
        """
        if self.__colourPegMapping is None:
            self.__colourPegMapping = {
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
            if i not in self.__colourPegMapping:
                colour = "#" + "".join([choice("0123456789ABCDEF") for _ in range(6)])
                if colour not in self.__colourPegMapping.values():
                    self.__colourPegMapping[i] = colour

    def __drawRow(self, root, row: list[int]) -> tk.Canvas:
        """
        Creates a canvas object and draws the row to it.
        """
        HEIGHTOFPEG = 100
        WIDTHOFPEG = 100
        SPACING = 18.75
        widthofrow = len(row) * (WIDTHOFPEG + SPACING) + SPACING
        heightofrow = HEIGHTOFPEG + SPACING * 2
        canvas = tk.Canvas(
            root,
            width=widthofrow,
            height=heightofrow,
            highlightthickness=1,
            highlightbackground="black",
        )
        for x, peg in enumerate(row):
            if peg not in self.__colourPegMapping:
                self.__genColourPegMapping([peg])
            canvas.create_oval(
                x * (WIDTHOFPEG + SPACING) + SPACING,
                SPACING,
                (x + 1) * (WIDTHOFPEG + SPACING),
                HEIGHTOFPEG + SPACING,
                fill=self.__colourPegMapping[peg],
            )
        return canvas

    def __drawResult(self, root, lenOfGuess: int, result: list[int]) -> tk.Canvas:
        """
        Creates a canvas object and draws the result to it.
        """
        COLOURMAPPING = {
            0: "#000000",
            1: "#FF0000",
            2: "#FFFFFF",
        }
        HEIGHTOFPEG = 50
        WIDTHOFPEG = 50
        SPACING = 12.5
        while len(result) < lenOfGuess:
            result.append(0)
        if (lenOfGuess % 2) == 1:
            lenOfGuess += 1
        widthofrow = lenOfGuess / 2 * (WIDTHOFPEG + SPACING) + SPACING
        heightofrow = 2 * (HEIGHTOFPEG + SPACING) + SPACING
        canvas = tk.Canvas(
            root,
            width=widthofrow,
            height=heightofrow,
            highlightthickness=1,
            highlightbackground="black",
        )
        for x, peg in enumerate(result[: lenOfGuess // 2]):
            canvas.create_oval(
                x * (WIDTHOFPEG + SPACING) + SPACING,
                SPACING,
                (x + 1) * (WIDTHOFPEG + SPACING),
                HEIGHTOFPEG + SPACING,
                fill=COLOURMAPPING[peg],
            )
        for x, peg in enumerate(result[lenOfGuess // 2 :]):
            canvas.create_oval(
                x * (WIDTHOFPEG + SPACING) + SPACING,
                HEIGHTOFPEG + SPACING * 2,
                (x + 1) * (WIDTHOFPEG + SPACING),
                (HEIGHTOFPEG + SPACING) * 2,
                fill=COLOURMAPPING[peg],
            )
        return canvas

    def displayRoundWinner(self, winner: Player):
        """
        Displays the winner of the round to the ui.
        """
        raise NotImplementedError()

    def displayWinner(self, winner: Player | None):
        """
        Displays the winner to the ui
        """
        raise NotImplementedError()

    def run(self):
        """
        Runs the GUI on a separate thread
        """
        # creates the actual root window and sets it up
        self.__realRoot = tk.Tk()
        self.__realRoot.state("zoomed")
        self.__realRoot.protocol("WM_DELETE_WINDOW", self.__onClosing)
        self.__realRoot.title(f"Mastermind - {self._playerName}")
        # creates and configures the virtual root window and scroll bars
        canvas = tk.Canvas(self.__realRoot, borderwidth=0, background="#ffffff")
        self.__root = tk.Frame(canvas, background="#ffffff")
        vsb = tk.Scrollbar(self.__realRoot, orient=tk.VERTICAL, command=canvas.yview)
        hsb = tk.Scrollbar(self.__realRoot, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.configure(xscrollcommand=hsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_window((4, 4), window=self.__root, anchor=tk.NW)
        self.__root.bind(
            "<Configure>", lambda event, canvas=canvas: self.__onFrameConfigure(canvas)
        )
        # set ready variable to true, start mainloop
        self.__ready = True
        self.__realRoot.mainloop()

    def __onClosing(self):
        """
        Overwrites the default closing behaviour of the window.
        Introduces a confirmation that the user wants to close the window.
        """
        if tkmb.askokcancel("Quit", "Do you want to quit?"):
            self.__realRoot.destroy()

    def __onFrameConfigure(self, canvas):
        """
        Whenever the frame is resized, this method is called.
        This is in order to update the scroll region to encompass the inner frame.
        """
        canvas.configure(scrollregion=canvas.bbox("all"))


class NetworkingHuman(Human):
    """
    Networking human class that inherits from the Human class
    """

    def __init__(self, playerName: str):
        super().__init__(playerName)
        pass


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

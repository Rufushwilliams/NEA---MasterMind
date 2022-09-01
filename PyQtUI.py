from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


class pegWidget(qtw.QFrame):
    def __init__(self, colour, value: int, small=False):
        super().__init__()
        if small:
            self.setFixedSize(50, 50)
        else:
            self.setFixedSize(100, 100)
        self.borderRadius = self.width() / 2
        self.updatePeg(colour, value)

    def setColour(self, colour):
        self.colour = colour
        self.updateStyleSheet()

    def updateStyleSheet(self):
        self.setStyleSheet(
            f"border-radius: {self.borderRadius}px; border: 1px solid black; background-color: {self.colour};"
        )

    def updatePeg(self, colour, value: int):
        self.value = value
        self.setColour(colour)


class resultWidget(qtw.QWidget):
    def __init__(self, lenOfGuess: int, result: list[int]):
        super().__init__()
        self.__lenOfGuess = lenOfGuess
        self.__result = result
        self.__colourMapping = {0: "#000000", 1: "#ff0000", 2: "#ffffff"}
        self.initWidget()
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        # create layout
        layout = qtw.QGridLayout()
        # fill the empty space with pegs
        while len(self.__result) < self.__lenOfGuess:
            self.__result.append(0)
        if (self.__lenOfGuess % 2) == 1:
            self.__lenOfGuess += 1
        # add pegs to layout
        for i, peg in enumerate(self.__result[: self.__lenOfGuess // 2]):
            layout.addWidget(
                pegWidget(self.__colourMapping[peg], peg, small=True), 0, i
            )
        for i, peg in enumerate(self.__result[self.__lenOfGuess // 2 :]):
            layout.addWidget(
                pegWidget(self.__colourMapping[peg], peg, small=True), 1, i
            )
        # add layout to widget
        self.setLayout(layout)


class guessWidget(qtw.QWidget):
    def __init__(self, guess: list[int], colourMapping: dict[int, str]):
        super().__init__()
        self.__guess = guess
        self.colourMapping = colourMapping
        self.lenOfGuess = len(guess)
        self.pegs: list[pegWidget] = []
        self.initWidget()
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        layout = qtw.QHBoxLayout()
        for peg in self.__guess:
            p = pegWidget(self.colourMapping[peg], peg)
            self.pegs.append(p)
            layout.addWidget(p)
        # add layout to widget
        self.setLayout(layout)


class mysteryPegWidget(qtw.QFrame):
    def __init__(self, colour, value: int):
        super().__init__()
        self.setFixedSize(100, 100)
        self.defaultColour = colour
        self.borderRadius = self.width() / 2
        self.updatePeg(colour, value)

    def setColour(self, colour):
        self.colour = colour
        if colour == self.defaultColour:
            # add QUESTION MARK
            pass
        self.updateStyleSheet()

    def updateStyleSheet(self):
        self.setStyleSheet(
            f"border-radius: {self.borderRadius}px; border: 1px solid black; background-color: {self.colour};"
        )

    def updatePeg(self, colour, value: int):
        self.value = value
        self.setColour(colour)


class hiddenCodeWidget(qtw.QWidget):
    def __init__(self, lenOfCode: int, colourMapping: dict[int, str]):
        super().__init__()
        self.colourMapping = colourMapping
        self.lenOfGuess = lenOfCode
        self.pegs: list[pegWidget] = []
        self.initWidget()
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        layout = qtw.QHBoxLayout()
        for _ in range(self.lenOfGuess):
            p = mysteryPegWidget(self.colourMapping[0], 0)
            self.pegs.append(p)
            layout.addWidget(p)
        self.setLayout(layout)


class guessResultWidget(qtw.QWidget):
    def __init__(
        self, guess: list[int], result: list[int], colourMapping: dict[int, str]
    ):
        super().__init__()
        self.__guess = guess
        self.lenOfGuess = len(guess)
        self.__result = result
        self.colourMapping = colourMapping
        self.initWidget()
        self.setContentsMargins(0, -12, 0, -12)
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        # create layout
        layout = qtw.QHBoxLayout()
        # add guess widget to layout
        self.gw = guessWidget(self.__guess, self.colourMapping)
        layout.addWidget(self.gw)
        # add result widget to layout
        layout.addWidget(resultWidget(len(self.__guess), self.__result))
        # add layout to widget
        self.setLayout(layout)


class boardWidget(qtw.QWidget):
    """
    Widget that contains the guesses and results of the game.
    Also generates the code widget and the input widgets.
    Stores them in codeWidget and inputs respectively.
    """

    def __init__(
        self,
        guesses: list[list[int]],
        results: list[list[int]],
        lenOfGuess: int,
        remainingGuesses: int,
        colourMapping: dict[int, str],
        code: list[int] = None,
        codeEditable: bool = False,
        guessEditable: bool = False,
        signal: qtc.pyqtSignal = None,
    ):
        super().__init__()
        self.__guesses = guesses
        self.__results = results
        self.__lenOfGuess = lenOfGuess
        self.__remainingGuesses = remainingGuesses
        self.__colourMapping = colourMapping
        self.__code = code
        self.__codeEditable = codeEditable
        self.__guessEditable = guessEditable
        self.signal = signal
        self.inputs = None
        self.initWidget()
        self.setFixedWidth(self.sizeHint().width() + 60)
        self.setSizePolicy(
            qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Expanding
        )

    def initWidget(self):
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        layout.setDirection(qtw.QBoxLayout.Direction.BottomToTop)
        for guess, result in zip(self.__guesses, self.__results):
            layout.addWidget(guessResultWidget(guess, result, self.__colourMapping))
        for i in range(self.__remainingGuesses):
            w = guessResultWidget(
                [0 for _ in range(self.__lenOfGuess)], [], self.__colourMapping
            )
            layout.addWidget(w)
            if i == 0 and self.__guessEditable:
                self.inputs = pegInputGenerator(self.signal, grw=w)

        if self.__code:
            self.codeWidget = guessWidget(self.__code, self.__colourMapping)
        else:
            self.codeWidget = hiddenCodeWidget(self.__lenOfGuess, self.__colourMapping)
        if self.__codeEditable:
            self.inputs = pegInputGenerator(self.signal, gw=self.codeWidget)
        self.codeWidget = scrollArea(self.codeWidget)
        if not self.inputs:
            w = guessResultWidget(
                [0 for _ in range(self.__lenOfGuess)], [], self.__colourMapping
            )
            self.inputs = pegInputGenerator(self.signal, grw=w)

        widget.setLayout(layout)
        layout = qtw.QHBoxLayout()
        layout.addWidget(scrollArea(widget))
        self.setLayout(layout)


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


class SignalsGUI(qtc.QObject):
    """
    A class that contains the signals used by the player GUI.
    """

    getMove = qtc.pyqtSignal(object)
    returnGuess = qtc.pyqtSignal(list)
    getCode = qtc.pyqtSignal(object)
    displayBoard = qtc.pyqtSignal(object, object)
    displayRoundWinner = qtc.pyqtSignal(object)
    displayWinner = qtc.pyqtSignal(object)


class loopSpinner(qtc.QEventLoop):
    """
    A class that is used by the GUI in order to listen for the returnGuess signal.
    """

    def __init__(self, gui):
        super().__init__()
        gui.signals.returnGuess.connect(self.listenForSignal)
        self.exec()

    @qtc.pyqtSlot(list)
    def listenForSignal(self, guess: list):
        self.result = guess
        self.quit()


class pegInput(qtw.QPushButton):
    def __init__(self, colour, value: int):
        super().__init__()
        self.value = value
        self.colour = colour
        self.setFixedSize(100, 100)
        self.borderRadius = self.width() / 2
        self.updateStyleSheet()

    def updateStyleSheet(self):
        self.setStyleSheet(
            f"border-radius: {self.borderRadius}px; border: 1px solid black; background-color: {self.colour};"
        )


class pegInputGenerator(qtc.QObject):
    """
    Creates buttons for the peg input.
    Links the buttons to the widget that is passed in.
    """

    def __init__(
        self,
        signal: qtc.pyqtSignal = None,
        grw: guessResultWidget = None,
        gw: guessWidget = None,
    ):
        super().__init__()
        if grw:
            self.widget = grw
            self.pegs = grw.gw.pegs
        elif gw:
            self.widget = gw
            self.pegs = gw.pegs
        else:
            raise TypeError("Either grw or gw must be passed in.")
        self.signal = signal
        self.__lenOfGuess = self.widget.lenOfGuess
        self.__colourMapping = self.widget.colourMapping
        self.__pegPointer = 0
        self.initWidget()

    def initWidget(self):

        self.pegButtons = []
        for value, colour in self.__colourMapping.items():
            if value == 0:
                continue
            button = pegInput(colour, value)
            button.clicked.connect(
                lambda state, colour=colour, value=value: self.onClick(colour, value)
            )
            self.pegButtons.append(button)

        self.fnButtons = []
        buttonc = qtw.QPushButton("Clear")
        buttonc.clicked.connect(self.onClear)
        buttonf = qtw.QPushButton("Print Values")
        buttonf.clicked.connect(self.getValues)
        self.fnButtons.append(buttonc)
        self.fnButtons.append(buttonf)

    def onClick(self, colour: str, value: int):
        # find the first peg that is not black and replace it with the colour
        self.pegs[self.__pegPointer].updatePeg(colour, value)
        self.__updatePegPointer()
        self.widget.update()

    def __updatePegPointer(self):
        if self.__pegPointer < self.__lenOfGuess - 1:
            self.__pegPointer += 1
        else:
            self.__pegPointer = 0

    def __clearButtonBindings(self):
        for button in self.pegButtons:
            button.clicked.disconnect()
        for button in self.fnButtons:
            button.clicked.disconnect()

    def onClear(self):
        self.__pegPointer = 0
        for peg in self.pegs:
            peg.updatePeg(self.__colourMapping[0], 0)
        self.widget.update()

    def getValues(self):
        pegValues = [peg.value for peg in self.pegs]
        if 0 not in pegValues and self.signal:
            self.__clearButtonBindings()
            self.signal.emit(pegValues)


class gameWidget(qtw.QWidget):
    def __init__(
        self,
        guesses: list[list[int]],
        results: list[list[int]],
        lenOfGuess: int,
        remainingGuesses: int,
        colourMapping: dict[int, str],
        code: list[int] = None,
        codeEditable: bool = False,
        guessEditable: bool = False,
        signal: qtc.pyqtSignal = None,
    ):
        super().__init__()
        self.__guesses = guesses
        self.__results = results
        self.__lenOfGuess = lenOfGuess
        self.__remainingGuesses = remainingGuesses
        self.__colourMapping = colourMapping
        self.__code = code
        self.__codeEditable = codeEditable
        self.__guessEditable = guessEditable
        self.__signal = signal
        self.initWidget()

    def initWidget(self):
        bw = boardWidget(
            self.__guesses,
            self.__results,
            self.__lenOfGuess,
            self.__remainingGuesses,
            self.__colourMapping,
            self.__code,
            self.__codeEditable,
            self.__guessEditable,
            self.__signal,
        )
        pegButtons = bw.inputs.pegButtons
        fnButtons = bw.inputs.fnButtons
        cw = bw.codeWidget
        primaryLayout = qtw.QGridLayout()
        pegButtonLayout = qtw.QGridLayout()
        if len(pegButtons) > 7:
            for i, button in enumerate(pegButtons):
                pegButtonLayout.addWidget(button, i // 2, i % 2)
        else:
            for i, button in enumerate(pegButtons):
                pegButtonLayout.addWidget(button, i, 0)
        pegButtonWidget = qtw.QWidget()
        pegButtonWidget.setLayout(pegButtonLayout)
        pegButtonWidget.setFixedSize(pegButtonWidget.sizeHint())
        pegButtonWidget = scrollArea(pegButtonWidget)

        fnButtonLayout = qtw.QHBoxLayout()
        for button in fnButtons:
            fnButtonLayout.addWidget(button)
        primaryLayout.addWidget(bw, 0, 0, 5, 4)
        primaryLayout.addWidget(pegButtonWidget, 0, 4, 5, 1)
        primaryLayout.addWidget(cw, 0, 5, 1, 3)
        primaryLayout.addLayout(fnButtonLayout, 1, 5, 1, 3)
        ##############################################################################
        # TODO: ADD A WIDGET THAT CAN BE USED TO WRITE ON                            #
        # TODO: E.G. Write enter your guess {num} or write the winners of the rounds #
        ##############################################################################
        self.setLayout(primaryLayout)


if __name__ == "__main__":

    ############################
    # TODO: TIDY UP WHOLE FILE #
    # TODO: ORGANISE CODE      #
    ############################

    lenOfGuess = 4
    colourMapping = {
        0: "#000000",
        1: "#ff0000",
        2: "#00ff00",
        3: "#0000ff",
        4: "#ffff00",
        5: "#00ffff",
        6: "#ff00ff",
    }

    app = qtw.QApplication([])
    mw = qtw.QMainWindow()
    mw.setWindowTitle("Test")

    widget = boardWidget([[1, 2, 3, 4]], [[]], 4, 4, colourMapping)

    mw.setCentralWidget(widget)
    mw.showMaximized()
    app.exec()

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


class pegWidget(qtw.QFrame):
    def __init__(self, colour, value: int, small=False):
        super().__init__()
        self.value = value
        if small:
            self.setFixedSize(50, 50)
        else:
            self.setFixedSize(100, 100)
        self.borderRadius = self.width() / 2
        self.colour = colour
        self.updateStyleSheet()

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
        self.__colourMapping = {0: "black", 1: "red", 2: "white"}
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
        self.__colourMapping = colourMapping
        self.pegs: list[pegWidget] = []
        self.initWidget()
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        layout = qtw.QHBoxLayout()
        for peg in self.__guess:
            p = pegWidget(self.__colourMapping[peg], peg)
            self.pegs.append(p)
            layout.addWidget(p)
        # add layout to widget
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
    ##################################################################
    # TODO: ADD CODE DISPLAYING                                      #
    # TODO: ORGANISE THE INPUT BUTTONS                               #
    # TODO: MAKE IT SO ENTERING THE CODE AND THE GUESS ARE DIFFERENT #
    # TODO: LOCK THE BOARD IF THE PLAYER ENTERED THE CODE            #
    ##################################################################
    def __init__(
        self,
        guesses: list[list[int]],
        results: list[list[int]],
        lenOfGuess: int,
        remainingGuesses: int,
        colourMapping: dict[int, str],
        code: list[int] = None,
        signal: qtc.pyqtSignal = None,
    ):
        super().__init__()
        self.__guesses = guesses
        self.__results = results
        self.__lenOfGuess = lenOfGuess
        self.__remainingGuesses = remainingGuesses
        self.__colourMapping = colourMapping
        self.signal = signal
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
        for i in range(self.__remainingGuesses - 1):
            w = guessResultWidget(
                [0 for _ in range(self.__lenOfGuess)], [], self.__colourMapping
            )
            layout.addWidget(w)
            if i == 0:
                self.inputs = pegInputGenerator(self.signal, w)

        #########################################
        layout2 = qtw.QVBoxLayout()
        layout3 = qtw.QHBoxLayout()
        for button in self.inputs.pegButtons:
            layout3.addWidget(button)
        layout4 = qtw.QHBoxLayout()
        for button in self.inputs.fnButtons:
            layout4.addWidget(button)
        layout2.addLayout(layout3)
        layout2.addLayout(layout4)
        ###########################################

        layout.addLayout(layout2)
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

    getMove = qtc.pyqtSignal(int, int, bool)
    returnGuess = qtc.pyqtSignal(list)
    getCode = qtc.pyqtSignal(int, int, bool)
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

    def __init__(self, signal: qtc.pyqtSignal, grw: guessResultWidget):
        super().__init__()
        self.signal = signal
        self.grw = grw
        self.pegs = grw.gw.pegs
        self.__lenOfGuess = grw.lenOfGuess
        self.__colourMapping = grw.colourMapping
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
        self.grw.update()

    def __updatePegPointer(self):
        if self.__pegPointer < self.__lenOfGuess - 1:
            self.__pegPointer += 1
        else:
            self.__pegPointer = 0

    def onClear(self):
        self.__pegPointer = 0
        for peg in self.pegs:
            peg.updatePeg(self.__colourMapping[0], 0)
        self.grw.update()

    def getValues(self):
        pegValues = [peg.value for peg in self.pegs]
        if 0 not in pegValues:
            self.signal.emit(pegValues)


if __name__ == "__main__":

    lenOfGuess = 4
    colourMapping = {
        0: "Black",
        1: "Red",
        2: "Yellow",
        3: "Green",
        4: "Blue",
        5: "orange",
    }

    app = qtw.QApplication([])
    mw = qtw.QMainWindow()
    mw.setWindowTitle("Test")

    widget = boardWidget([[1, 2, 3, 4]], [[]], 4, 4, colourMapping)

    mw.setCentralWidget(widget)
    mw.showMaximized()
    app.exec()

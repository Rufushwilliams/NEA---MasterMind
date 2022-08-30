from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc



class pegWidget(qtw.QFrame):
    def __init__(self, color, small=False):
        super().__init__()
        if small:
            self.setFixedSize(50, 50)
        else:
            self.setFixedSize(100, 100)
        borderRadius = self.width() / 2
        self.setStyleSheet(
            f"border-radius: {borderRadius}px; border: 1px solid black; background-color: {color}"
        )


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
            layout.addWidget(pegWidget(self.__colourMapping[peg], small=True), 0, i)
        for i, peg in enumerate(self.__result[self.__lenOfGuess // 2 :]):
            layout.addWidget(pegWidget(self.__colourMapping[peg], small=True), 1, i)
        # add layout to widget
        self.setLayout(layout)


class guessWidget(qtw.QWidget):
    def __init__(self, guess: list[int], colourMapping: dict[int, str]):
        super().__init__()
        self.__guess = guess
        self.__colourMapping = colourMapping
        self.initWidget()
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        layout = qtw.QHBoxLayout()
        for peg in self.__guess:
            layout.addWidget(pegWidget(self.__colourMapping[peg]))
        # add layout to widget
        self.setLayout(layout)


class guessResultWidget(qtw.QWidget):
    def __init__(
        self, guess: list[int], result: list[int], colourMapping: dict[int, str]
    ):
        super().__init__()
        self.__guess = guess
        self.__result = result
        self.__colourMapping = colourMapping
        self.initWidget()
        self.setContentsMargins(0, -12, 0, -12)
        self.setFixedSize(self.sizeHint())

    def initWidget(self):
        # create layout
        layout = qtw.QHBoxLayout()
        # add guess widget to layout
        layout.addWidget(guessWidget(self.__guess, self.__colourMapping))
        # add result widget to layout
        layout.addWidget(resultWidget(len(self.__guess), self.__result))
        # add layout to widget
        self.setLayout(layout)


class boardWidget(qtw.QWidget):
    #############################
    # TODO: ADD CODE DISPLAYING #
    #############################
    def __init__(
        self,
        guesses: list[list[int]],
        results: list[list[int]],
        lenOfGuess: int,
        remainingGuesses: int,
        colourMapping: dict[int, str],
        code: list[int] = None,
    ):
        super().__init__()
        self.__guesses = guesses
        self.__results = results
        self.__lenOfGuess = lenOfGuess
        self.__remainingGuesses = remainingGuesses
        self.__colourMapping = colourMapping
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
        for _ in range(self.__remainingGuesses):
            layout.addWidget(
                guessResultWidget(
                    [0 for _ in range(self.__lenOfGuess)], [], self.__colourMapping
                )
            )
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

from typing import Callable

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw


class pegWidget(qtw.QFrame):
    def __init__(self, colour, value: int, small=False):
        super().__init__()
        if small:
            self.setFixedSize(50, 50)
        else:
            self.setFixedSize(100, 100)
        self.borderRadius = self.width() // 2
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

    def getColourValue(self) -> tuple[str, int]:
        """Returns a tuple of the colour and value of the peg"""
        return self.colour, self.value


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
            # TODO: add QUESTION MARK
            pass
        self.updateStyleSheet()

    def updateStyleSheet(self):
        self.setStyleSheet(
            f"border-radius: {self.borderRadius}px; border: 1px solid black; background-color: {self.colour};"
        )

    def updatePeg(self, colour, value: int):
        self.value = value
        self.setColour(colour)

    def getColourValue(self) -> tuple[str, int]:
        """Returns a tuple of the colour and value of the peg"""
        return self.colour, self.value


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
        self,
        guess: list[int],
        result: list[int],
        colourMapping: dict[int, str],
        num: int = None,
    ):
        super().__init__()
        self.__num = num
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
        if self.__num:
            layout.addWidget(qtw.QLabel(f"{self.__num}"))
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

    ###########################################
    # GROUP B SKILL: MULTI-DIMENSIONAL ARRAYS #
    ###########################################
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
        duplicatesAllowed: bool = True,
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
        self.__duplicatesAllowed = duplicatesAllowed
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
        for i, (guess, result) in enumerate(zip(self.__guesses, self.__results)):
            layout.addWidget(
                guessResultWidget(guess, result, self.__colourMapping, i + 1)
            )
        for i in range(self.__remainingGuesses):
            w = guessResultWidget(
                [0 for _ in range(self.__lenOfGuess)],
                [],
                self.__colourMapping,
                i + 1 + len(self.__guesses),
            )
            layout.addWidget(w)
            if i == 0 and self.__guessEditable:
                self.inputs = pegInputGenerator(
                    self.signal, grw=w, duplicatesAllowed=self.__duplicatesAllowed
                )

        if self.__code:
            self.codeWidget = guessWidget(self.__code, self.__colourMapping)
        else:
            self.codeWidget = hiddenCodeWidget(self.__lenOfGuess, self.__colourMapping)
        if self.__codeEditable:
            self.inputs = pegInputGenerator(
                self.signal,
                gw=self.codeWidget,
                duplicatesAllowed=self.__duplicatesAllowed,
            )
        cwHeight = self.codeWidget.sizeHint().height()
        self.codeWidget = scrollArea(self.codeWidget)
        self.codeWidget.setFixedHeight(cwHeight + 25)
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


class buttonSubmit(qtw.QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.commands: list[Callable] = []
        self.clicked.connect(self.executeCommands)

    def executeCommands(self):
        for command in self.commands:
            x = command()
            if x is False:
                break

    def addCommand(self, command: Callable):
        self.commands.append(command)


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
        duplicatesAllowed: bool = True,
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
        self.__duplicatesAllowed = duplicatesAllowed
        self.__lenOfGuess = self.widget.lenOfGuess
        self.__colourMapping = self.widget.colourMapping
        self.__pegPointer = 0
        self.__stack = []
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

        self.fnButtons = {}
        buttonu = qtw.QPushButton("Undo")
        buttonu.clicked.connect(self.onUndo)
        buttonc = qtw.QPushButton("Clear")
        buttonc.clicked.connect(self.onClear)
        buttonf = buttonSubmit("Submit")
        buttonf.addCommand(lambda: self.getValues(self.__duplicatesAllowed))
        self.fnButtons["Undo"] = buttonu
        self.fnButtons["Clear"] = buttonc
        self.fnButtons["Submit"] = buttonf

    def __clearButtonBindings(self):
        for button in self.pegButtons:
            button.clicked.disconnect()
        for button in self.fnButtons.values():
            button.clicked.disconnect()

    def onClick(self, colour: str, value: int):
        """
        Changes the colour of the peg that is currently selected.
        """
        # add the current state of the peg to the stack
        self.__addMoveToStack(*self.pegs[self.__pegPointer].getColourValue())
        # find the next peg using the pegPointer and replace it with the colour
        self.pegs[self.__pegPointer].updatePeg(colour, value)
        self.__updatePegPointer()
        self.widget.update()

    def __updatePegPointer(self):
        if self.__pegPointer < self.__lenOfGuess - 1:
            self.__pegPointer += 1
        else:
            self.__pegPointer = 0

    ###################################
    # GROUP A SKILL: STACK OPERATIONS #
    ###################################

    def __addMoveToStack(self, oldColour: str, oldValue: int):
        self.__stack.append((self.__pegPointer, oldColour, oldValue))

    def __addClearToStack(self):
        # add the current state of the pegs to the stack
        pegColourValues = []
        for peg in self.pegs:
            pegColourValues.append(peg.getColourValue())
        self.__stack.append((self.__pegPointer, pegColourValues))

    def onUndo(self):
        # undo the last move
        if len(self.__stack) > 0:
            move = self.__stack.pop()
            if len(move) == 3:
                self.__pegPointer, oldColour, oldValue = move
                self.pegs[self.__pegPointer].updatePeg(oldColour, oldValue)
            elif len(move) == 2:
                self.__pegPointer, pegColourValues = move
                for peg, colourValue in zip(self.pegs, pegColourValues):
                    peg.updatePeg(*colourValue)
            self.widget.update()

    def onClear(self):
        self.__addClearToStack()
        self.__pegPointer = 0
        for peg in self.pegs:
            peg.updatePeg(self.__colourMapping[0], 0)
        self.widget.update()

    def getValues(self, duplicatesAllowed: bool):
        pegValues = [peg.value for peg in self.pegs]
        if (0 not in pegValues and self.signal) and (
            duplicatesAllowed or len(set(pegValues)) == len(pegValues)
        ):
            self.__clearButtonBindings()
            self.signal.emit(pegValues)
        else:
            return False


class messageWidget(qtw.QFrame):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
        self.initWidget()
        self.setFrameShape(qtw.QFrame.Shape.Box)
        self.sizePolicy = qtw.QSizePolicy()
        self.sizePolicy.setHorizontalPolicy(qtw.QSizePolicy.Policy.Expanding)
        self.sizePolicy.setVerticalPolicy(qtw.QSizePolicy.Policy.Expanding)
        self.setSizePolicy(self.sizePolicy)

    def initWidget(self):
        layout = qtw.QVBoxLayout()
        label = qtw.QLabel(self.message)
        label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

    def updateMessage(self, message: str):
        self.message = message
        self.layout().itemAt(0).widget().setText(message)
        self.update()


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
        duplicatesAllowed: bool = True,
        message: str = None,
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
        self.__duplicatesAllowed = duplicatesAllowed
        self.__message = message
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
            self.__duplicatesAllowed,
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

        self.messageWidget = messageWidget(self.__message)

        fnButtonLayout = qtw.QHBoxLayout()
        fnButtons["Submit"].addCommand(
            lambda w=self.messageWidget: w.updateMessage("Waiting for other player...")
        )
        for button in fnButtons.values():
            fnButtonLayout.addWidget(button)
        primaryLayout.addWidget(bw, 0, 0, 5, 4)
        primaryLayout.addWidget(pegButtonWidget, 0, 4, 5, 1)
        primaryLayout.addWidget(cw, 0, 5, 1, 3)
        primaryLayout.addLayout(fnButtonLayout, 1, 5, 1, 3)
        primaryLayout.addWidget(self.messageWidget, 2, 5, 3, 3)
        self.setLayout(primaryLayout)

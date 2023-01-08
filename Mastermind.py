from sys import argv

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from UI import GUI, Terminal


def usage():
    print(
        f"""
    Usage: {argv[0]} [g | t]
    g : play with the GUI
    t : play with the Terminal"""
    )
    quit()


if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    if argv[1] == "t":
        ui = Terminal()
        ui.run()
    elif argv[1] == "g":
        app = QApplication([])
        ui = GUI()
        timer = QTimer()
        timer.singleShot(100, ui.run)
        app.exec()
    else:
        usage()

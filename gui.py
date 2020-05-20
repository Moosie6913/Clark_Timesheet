from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    xpos, width = 200,300
    ypos, height = 200, 300
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(xpos, ypos, width, height)
    win.setWindowTitle("TITLE TO BE CONFIRMED")

    label = QtWidgets.QLabel(win)
    label.setText("my first label")
    label.move(50,50)

    win.show()
    sys.exit(app.exec_())

window()
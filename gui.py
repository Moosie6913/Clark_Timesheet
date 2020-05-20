from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        width, height = 600, 400
        self.setGeometry(300,300,width,height)
        self.setFixedSize(width,height)
        self.setWindowTitle("Automation")
        # self.setWindowIcon(QtWidgets.Qicon'/include/icon.png')

        # Set up ActionBars
        # User Preferences
        user_preferences_action = QtWidgets.QAction("User Preferences",self)
        user_preferences_action.setShortcut("Ctrl+U")
        user_preferences_action.setStatusTip("Modify User Configured Settings")
        user_preferences_action.triggered.connect(self.user_preferences)
        #Log in Credentials
        credential_action = QtWidgets.QAction("Credential Settings",self)
        credential_action.setShortcut("Ctrl+Y")
        credential_action.setStatusTip("Modify or Delete Login Information")
        credential_action.triggered.connect(CredentialWindow.show())


        self.statusBar()

        mainMenu = self.menuBar()
        settingsMenu = mainMenu.addMenu('&Settings')
        settingsMenu.addAction(user_preferences_action)
        settingsMenu.addAction(credential_action)



        # Open up Home/Main Window
        self.Home()

    def Home(self):
        btn = QtWidgets.QPushButton("Quit",self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(520,370)
        self.show()

    def user_preferences(self):
        pass


    def close_application(self):
        print("Closeing")
        sys.exit()


class CredentialWindow(QDialog):

    def __init__(self):
        super().__init__()
        #self.win1 = QtWidget()
        width, height = 600, 400
        self.setGeometry(35, 350, width, height)
        self.setFixedSize(width, height)
        self.setWindowTitle("NewWindow")
        self.test()
        # def credential_settings(self):
        #     pass

    def test(self):
        btn = QtWidgets.QPushButton("Quit", self)
        btn.clicked.connect(self.blank)
        btn.resize(btn.minimumSizeHint())
        btn.move(520, 370)
        self.show()

    def blank(self):
        pass


def run():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

# def window():
#     xpos, width = 200,300
#     ypos, height = 200, 300
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     win.setGeometry(xpos, ypos, width, height)
#     win.setWindowTitle("TITLE TO BE CONFIRMED")
#
#     label = QtWidgets.QLabel(win)
#     label.setText("my first label")
#     label.move(50,50)
#
#     win.show()
#     sys.exit(app.exec_())
#Clean looks or Plastique
#window()
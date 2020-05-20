from PyQt5 import QtWidgets
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
#import breeze_resources
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        width, height = 600, 400
        self.setGeometry(300,300,width,height)
        self.setFixedSize(width,height)
        self.setWindowTitle("Automation")
        # self.setWindowIcon(QtWidgets.Qicon'/include/icon.png')

        #HOME
        self.label = QtWidgets.QLabel(self)
        self.label.setText("my First Label")
        self.label.move(50,50)
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText("Hide All")
        self.btn.resize(self.btn.minimumSizeHint())
        self.btn.move(220,270)
        #self.btn.clicked.connect(self.makehide)
        #
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText("Show")
        self.btn1.resize(self.btn.minimumSizeHint())
        self.btn1.move(300,270)

        #USER PREF

        self.lb_User_Header = QtWidgets.QLabel(self)
        self.lb_User_Header.setText("User Preferences")
        self.lb_User_Header.move(20,20)

        self.lb_User_Name = QtWidgets.QLabel(self)
        self.lb_User_Name.setText("Name:")
        self.lb_User_Name.move(20,55)

        self.txtb_User_Name = QtWidgets.QLineEdit(self)
        self.txtb_User_Name.setPlaceholderText("Enter your first name")
        self.txtb_User_Name.setGeometry(0,0,150,20)
        self.txtb_User_Name.move(60,60)

        self.btn_User_Save = QtWidgets.QPushButton(self)
        self.btn_User_Save.setText("Save")
        self.btn_User_Save.move(470,350)
        self.btn_User_Save.clicked.connect(self.btn_user_save_clicked)

        self.lb_User_heritage = QtWidgets.QLabel(self)
        self.lb_User_heritage.setText("Heritage Timesheet Application:")
        self.lb_User_heritage.resize(self.lb_User_heritage.minimumSizeHint())
        self.lb_User_heritage.move(220,63)


        self.rb_User_heritage = QtWidgets.QButtonGroup(self)
        self.rb_User_heritage.buttonClicked[int].connect(self.rb_User_heritage_clicked)
        button = QtWidgets.QPushButton(self)
        button.setText("Worley")
        button.move(380,55)
        self.rb_User_heritage.addButton(button,1)

        button = QtWidgets.QPushButton(self)
        button.setText("ECR")
        button.move(480, 55)
        self.rb_User_heritage.addButton(button,2)



        self.lb_User_test = QtWidgets.QLabel(self)
        self.lb_User_test.setText("Blank:")
        self.lb_User_test.resize(self.lb_User_test.minimumSizeHint())
        self.lb_User_test.move(300,150)




        # Set up ActionBars
        home_action = QtWidgets.QAction("Home",self)
        home_action.setShortcut("Ctrl+H")
        home_action.setStatusTip("Home")
        home_action.triggered.connect(self.home)
        # User Preferences
        user_preferences_action = QtWidgets.QAction("User Preferences",self)
        user_preferences_action.setShortcut("Ctrl+U")
        user_preferences_action.setStatusTip("Modify User Configured Settings")
        user_preferences_action.triggered.connect(self.user_pref_tab)
        #Log in Credentials
        credential_action = QtWidgets.QAction("Credential Settings",self)
        credential_action.setShortcut("Ctrl+Y")
        credential_action.setStatusTip("Modify or Delete Login Information")
        #credential_action.triggered.connect(self.show)


        self.statusBar()

        mainMenu = self.menuBar()
        settingsMenu = mainMenu.addMenu('&Settings')
        settingsMenu.addAction(home_action)
        settingsMenu.addAction(user_preferences_action)
        settingsMenu.addAction(credential_action)
        # Open up Home/Main Window
        #self.home()

        # self.setLayout(self.hbox_User_Top)
        self.user_pref_tab()



    def home(self):
        self.allhide()
        self.label.setHidden(False)
        self.btn.setHidden(False)
        self.btn.setHidden(False)
        #self.btn1.clicked.connect(self.unhide)

        #self.show()


    def user_pref_tab(self):
        self.allhide()

        self.lb_User_Header.setHidden(False)
        self.lb_User_Name.setHidden(False)
        self.txtb_User_Name.setHidden(False)
        self.btn_User_Save.setHidden(False)
        self.lb_User_heritage.setHidden(False)
        #self.rb_User_heritage.setHidden(False)

        self.show()

    def allhide(self):
        # hide every single item
        #Home

        self.label.setHidden(True)
        self.btn.setHidden(True)
        self.btn1.setHidden(True)
        #User Pref

        self.lb_User_Header.setHidden(True)
        self.lb_User_Name.setHidden(True)
        self.txtb_User_Name.setHidden(True)
        self.btn_User_Save.setHidden(True)
        self.lb_User_heritage.setHidden(True)
        #self.rb_User_heritage.setHidden(True)

    def btn_user_save_clicked(self):
        print(self.txtb_User_Name.text())

    def rb_User_heritage_clicked(self, id):
        for button in self.rb_User_heritage.buttons():
            button.setStyleSheet("background-color: white")
            print(button)
            print(self.rb_User_heritage.buttons())
            if button is self.rb_User_heritage.button(id):
                button.setStyleSheet("background-color: red")
                #self.lb_User_test.setText(button.text())

def run():
    app = QApplication(sys.argv)
    win = MainWindow()
    print("closeing")
    sys.exit(app.exec_())



if __name__ == '__main__':
    run()

#Clean looks or Plastique
#window()
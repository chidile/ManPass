from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent

from ui.login_ui import Ui_Form
from main_window import MainWindow

from sql_class import ConnectMySQL

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        ## Initialize variables for mouse dragging
        self._startPos = None
        self._endPos = None
        self._tracking = False

        ## create database connection object
        self.db = ConnectMySQL()

        ## Initialize QPushbutton in login_ui.py
        self.ui.backBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.registerBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.exitBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.loginBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.createBtn.setFocusPolicy(Qt.NoFocus)


        ## show login page when you start the apps
        self.ui.funcWidget.setCurrentIndex(0)

        ## hide the window frame and background of the app
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)



    @pyqtSlot()
    def on_exitBtn_clicked(self):
        """function to exit the application when the exit button is clicked."""
        msg = QMessageBox(self)
        msg.setWindowIcon(QIcon("./static/icon/key-6-128.ico"))
        msg.setIconPixmap(QPixmap("./static/icon/question-mark-7-48.ico"))
        msg.setWindowTitle("Exit Application?")
        msg.setText("Are you sure you want to exit the application?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            self.close()
        else:
            return
        
    @pyqtSlot()
    def on_registerBtn_clicked(self):
        """ Function to switch to the registration page when the register button is clicked."""
        self.ui.funcWidget.setCurrentIndex(1)

    
    @pyqtSlot()
    def on_backBtn_clicked(self):
        """ Function to switch to the login page when the back button is clicked."""
        self.ui.funcWidget.setCurrentIndex(0)


    @pyqtSlot()
    def on_createBtn_clicked(self):
        """ Function to create a new user account when the create button is clicked."""
        username = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()

        if username and password:
            result = self.db.check_username(username)
            if result:
                self.warning_messageBox(f"Username {username} already exists! Please choose a different username.")
            else:
                result = self.db.create_login_account(user_name=username, password=password)
                if result:
                    content = f"Error creating account: {result}. Please try again."
                    self.warning_messageBox(content)
                else:
                    self.warning_messageBox("Account created successfully! You can now log in.")
                    
                    self.ui.lineEdit_3.clear()
                    self.ui.lineEdit_4.clear()
                    self.ui.funcWidget.setCurrentIndex(0)


    def warning_messageBox(self, content):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Warning!")
        msgBox.setText(content)
        msgBox.setStandardButtons(QMessageBox.Ok)

        msgBox.exec_()


    ## TODO: make window draggable
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._startPos = event.pos()
            self._tracking = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._tracking:
            self._endPos = event.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._tracking = False


        
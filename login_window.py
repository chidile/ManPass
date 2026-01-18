from PyQt5.QtWidgets import QWidget, QMessageBox,QPushButton
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
import traceback

from ui.login_ui import Ui_Form
from main_window import MainWindow

from sql_class import ConnectMySQL

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._startPos = None
        self._endPos = None
        self._tracking = False

        self.mysql = ConnectMySQL()

        ## Initialize QPushButton 
        self.ui.backBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.createBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.exitBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.registerBtn.setFocusPolicy(Qt.NoFocus)
        self.ui.loginBtn.setFocusPolicy(Qt.NoFocus)

        # show login page when you start the application
        self.ui.funcWidget.setCurrentIndex(0)

        ## hide the window frame and background of the app
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    @pyqtSlot()
    def on_exitBtn_clicked(self):
        """Exit the application when the exit button is clicked."""
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
        """Switch to the registration page when the register button is clicked."""
        self.ui.funcWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_loginBtn_clicked(self):
        """Function for login app."""
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()

        ## Check if username and password are not empty
        if not username or not password:
            print("Username or password is empty. Please provide both.")
            self.warning_messagebox(content="Please enter both username and password.")
            return
        
        ## Check username and password from database
        result = self.mysql.check_username(username=username)
        print(result)
        if result and len(result) == 1:
            if result[0]["password"] == password:
                user_id = result[0]["user_id"]

                # pass the user_id to main window and show it
                main_window = MainWindow(user_id=user_id)
                main_window.show()
                self.close()
            else:
                # print("Incorrect password. Please try again.")
                self.warning_messagebox(content="Incorrect password. Please try again.")
                self.ui.lineEdit_2.clear()
        else:
            # print("Username does not exist. Please try again.")
            self.warning_messagebox(content="Username does not exist. Please try again.")
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
                

    @pyqtSlot()
    def on_backBtn_clicked(self):
        """Switch back to the login page when the back button is clicked."""
        self.ui.funcWidget.setCurrentIndex(0)


    @pyqtSlot()
    def on_createBtn_clicked(self):
        """ Create a Login account """
        username = self.ui.lineEdit_3.text().strip()
        password = self.ui.lineEdit_4.text().strip()

        if username and password:
            ## Check if username exist on the database.
            result = self.mysql.check_username(username=username)
            print(f"Function: \n\nUsername:  {username} \n\nPassword: {password}")
            print(result)
            if result:
                print("Username already exists in database.")
                self.warning_messagebox(content=f"The {username} is already in database. Please try another one.")

            else:
                print("Username is available. Creating account...")
                ## Create login account
                result = self.mysql.create_login_account(user_name=username, password=password)

                if result: # if there is an error
                    print(f"Error creating login account: {result}")
                    content = f"Something is wrong: {result}. Please try again."
                    self.warning_messagebox(content=content)
                    
                else:
                    ## Successfully create login account, clear input and go back to login window
                    print("Successfully create login account.")
                    # self.warning_messagebox(content="Successfully create login account.")

                    self.ui.lineEdit_3.clear()
                    self.ui.lineEdit_4.clear()
                    self.ui.funcWidget.setCurrentIndex(0)

                    ## Create default configuration data for the new account
                    # get user_id
                    result_1 = self.mysql.check_username(username=username)
                    user_id =result_1[0]["user_id"]
                    result_2 = self.mysql.check_config_data(user_id=user_id)
                    if not result_2:
                        result3 = self.mysql.create_config_data(user_id=user_id)
                        if result3:
                            print(f"Error creating default configuration data: {result3}")
                            content = f"Something is wrong: {result3}. Please try again."
                            # self.warning_messagebox(content=content)
        elif username or password:
            print("Please enter your username or password.")
           
        else:
            self.warning_messagebox(content="Please enter both username and password.")
            print("Please enter both username and password.")



    ## Create QMessageBox
    def warning_messagebox(self, content):
        """ Common messagebox function. """
        msgBox = QMessageBox(self)
        msgBox.setWindowIcon(QIcon("./static/icon/key-6-128.ico"))
        msgBox.setIconPixmap(QPixmap("./static/icon/question-mark-7-48.ico"))
        msgBox.setWindowTitle("Warning")
        msgBox.setText(content)
        msgBox.setStandardButtons(QMessageBox.Close)

        msgBox.exec_()









    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._tracking:
            self._endPos = event.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._startPos = QPoint(event.x(), event.y())
            self._tracking = True

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QApplication, QTableWidgetItem,\
    QPushButton, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent

from ui.main_window_ui import Ui_MainWindow
from sql_class import ConnectMySQL

import random


class MainWindow(QMainWindow):
    def __init__(self, user_id=None):
        super(MainWindow, self).__init__()

        self.USER_ID = user_id
        self.mysql = ConnectMySQL()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## init widget in app
        self.show_pw_btn = self.ui.pushButton
        self.create_pw_btn = self.ui.pushButton_2
        self.conf_btn = self.ui.pushButton_3

        self.pages = self.ui.stackedWidget

        ## SHOW PASSWORD WINDOW
        self.website_show = self.ui.lineEdit_5
        self.userame_show = self.ui.lineEdit_4

        self.pw_table = self.ui.tableWidget

        ##Password generate window
        self.website_create = self.ui.lineEdit
        self.username_create = self.ui.lineEdit_2
        self.password_length = self.ui.spinBox
        self.lowercase_le = self.ui.checkBox
        self.uppercase_le = self.ui.checkBox
        self.lowercase_le = self.ui.checkBox
        

        ## Show the ppassword list page
        self.pages.setCurrentIndex(0)

        ## Connect signal and slot
        self.show_pw_btn.toggled.connect(lambda : self.do_change_page(self.show_pw_btn))
        self.create_pw_btn.toggled.connect(lambda : self.do_change_page(self.create_pw_btn))
        self.conf_btn.toggled.connect(lambda : self.do_change_page(self.conf_btn))

    @pyqtSlot()
    def on_exitBtn_clicked(self):
        """
        function for exit        
        """
    # Create a QMessageBox
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


    def do_change_page(self, btn):
        """
        Function to change page
        """
        btn_text = btn.text().strip()
        if btn_text == self.show_pw_btn.text().strip():
            self.pages.setCurrentIndex(0)
        elif btn_text == self.create_pw_btn.text().strip():
            self.pages.setCurrentIndex(1)
        else:
            self.pages.setCurrentIndex(2)


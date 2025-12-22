from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent

from ui.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self,):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## init widget in app
        self.show_pw_btn = self.ui.pushButton
        self.create_pw_btn = self.ui.pushButton_2
        self.conf_btn = self.ui.pushButton_3

        self.pages = self.ui.stackedWidget

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


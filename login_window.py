from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent

from ui.login_ui import Ui_Form
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._startPos = None
        self._endPos = None
        self._tracking = False

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
        """Switch to the main application page when the login button is clicked."""
        main_window = MainWindow()
        main_window.show()

        self.close()

    @pyqtSlot()
    def on_backBtn_clicked(self):
        """Switch back to the login page when the back button is clicked."""
        self.ui.funcWidget.setCurrentIndex(0)

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
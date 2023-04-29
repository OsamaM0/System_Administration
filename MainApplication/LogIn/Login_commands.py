import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from MainApplication.LogIn.LoginGUI import Ui_Form




from PyQt5 import QtCore, QtGui, QtWidgets


class Login(QtWidgets.QMainWindow):
    login_signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        # Create an instance of the login UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Load the image and set it as the pixmap for the QLabel widget
        pixmap = QPixmap('D:\Git Hub\Git_Hub\General_Management_Program\GUI\image\LogIn\Log_In_background.jpg')
        #pixmap = QPixmap(':/newPrefix/image/LogIn/Log_In_background.jpg')
        self.ui.background.setPixmap(pixmap)

        # Connect signals and slots
        self.ui.btn_login.clicked.connect(self.login)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)   
        self.ui.btn_close.clicked.connect(lambda: sys.exit())

    def login(self):
        # Get the user name and password from the UI
        username = self.ui.le_username.text()
        password = self.ui.le_password.text()

        # Emit the login signal
        self.login_signal.emit(username, password)
                

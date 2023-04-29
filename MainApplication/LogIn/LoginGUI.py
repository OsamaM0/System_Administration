# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1151, 619)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)
        Form.setStyleSheet("background-color:#FFFFFF;\n"
"border-radius:50px")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 10, 1111, 601))
        self.widget.setStyleSheet("background-color:#FFFFFF;\n"
"border-radius:50px")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(680, 180, 401, 201))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:1 rgba(245, 245, 245,250));\n"
"\n"
"border-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(680, 60, 400, 81))
        self.label_4.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.47191 rgba(89, 165, 142, 255), stop:1 rgba(184, 184, 184, 255))")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.le_username = QtWidgets.QLineEdit(self.widget)
        self.le_username.setGeometry(QtCore.QRect(740, 200, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.le_username.setFont(font)
        self.le_username.setStyleSheet("QLineEdit{\n"
"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom: 2px solid rgba(105,118,132,255);\n"
"color:rgb(0,0,0);\n"
"padding-bottom:7px;\n"
"}\n"
"QLineEdit:hover{\n"
"\n"
"background-color:#5EAAA8\n"
"border:none;\n"
"border-bottom: 2px solid rgba(105,118,132,255);\n"
"color:rgb(0,0,0);\n"
"padding-bottom:7px;\n"
"\n"
"}")
        self.le_username.setObjectName("le_username")
        self.le_password = QtWidgets.QLineEdit(self.widget)
        self.le_password.setGeometry(QtCore.QRect(740, 290, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.le_password.setFont(font)
        self.le_password.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom: 2px solid rgba(105,118,132,255);\n"
"color:rgb(0,0,0);\n"
"padding-bottom:7px;")
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password.setObjectName("le_password")
        self.btn_login = QtWidgets.QPushButton(self.widget)
        self.btn_login.setGeometry(QtCore.QRect(820, 410, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.btn_login.setFont(font)
        self.btn_login.setStyleSheet("\n"
"QPushButton#btn_login{\n"
"    \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.45,stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 95, 112, 226));\n"
"\n"
"color:rgba(255,255,255,210);\n"
"\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton#btn_login:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.45,stop:0 rgba(50, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"    \n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton#btn_login:pressed{\n"
"    \n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105,118,132,200);\n"
"}")
        self.btn_login.setObjectName("btn_login")
        self.btn_close = QtWidgets.QPushButton(self.widget)
        self.btn_close.setEnabled(True)
        self.btn_close.setGeometry(QtCore.QRect(1060, 20, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.btn_close.setFont(font)
        self.btn_close.setStyleSheet("\n"
"QPushButton#btn_close{\n"
"    \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.45,stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 0));\n"
"\n"
"color:rgba(100,100,100,100);\n"
"\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton#btn_close:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.45,stop:0 rgba(50, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"color:#FFFFFF\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton#btn_close:pressed{\n"
"    \n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105,118,132,200);\n"
"    color:#FFFFFF\n"
"\n"
"}")
        self.btn_close.setObjectName("btn_close")
        self.background = QtWidgets.QLabel(self.widget)
        self.background.setEnabled(True)
        self.background.setGeometry(QtCore.QRect(30, 20, 701, 571))
        self.background.setStyleSheet("background:url(:/newPrefix/image/LogIn/Log_In_background.jpg);\n"
"background-color:#FFFFFF;\n"
"border-radius:50px;")
        self.background.setText("")
        self.background.setScaledContents(False)
        self.background.setWordWrap(False)
        self.background.setObjectName("background")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(33, 10, 661, 20))
        self.label.setStyleSheet("background-color:#FFFFFF;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 30, 280))
        self.label_5.setStyleSheet("background-color:#FFFFFF;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(680, 20, 51, 161))
        self.label_3.setStyleSheet("background-color:#FFFFFF;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.background.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.le_password.raise_()
        self.le_username.raise_()
        self.btn_login.raise_()
        self.btn_close.raise_()
        self.label.raise_()
        self.label_5.raise_()
        self.label_3.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "اهلاً بيك"))
        self.le_username.setPlaceholderText(_translate("Form", "أسم المستخدم"))
        self.le_password.setPlaceholderText(_translate("Form", "كلمة المرور"))
        self.btn_login.setText(_translate("Form", "دخول"))
        self.btn_close.setText(_translate("Form", "X"))
import res_rc

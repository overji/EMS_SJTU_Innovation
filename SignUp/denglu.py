# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'denglu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from . import bg


class Ui_MainWindow1(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(747, 592)
        font = QtGui.QFont()
        font.setFamily("HONOR Sans Design Thin")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/新前缀/1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(
            "background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.431, fx:0.5, fy:0.5, stop:0.153409 rgba(39, 98, 216, 255), stop:1 rgba(16, 16, 181, 255));\\npadding:10px;\n"
            "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 440, 121, 60))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(280, 260, 291, 50))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 360, 111, 31))
        font = QtGui.QFont()
        font.setFamily("HONOR Sans Display GBK Medium")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 360, 111, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(320, 20, 121, 121))
        self.label_3.setStyleSheet("border-image: url(:/back/资源 1.png);\n"
                                   "border-image: url(:/新前缀/1x/1x/资源 1.png);\n"
                                   "background-color: rgba(0,0,0,0);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 170, 291, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(570, 270, 31, 21))
        self.pushButton_4.setStyleSheet("border-image: url(:/新前缀/1x/1x/资源 5.png);\n"
                                        "background-color: rgba(0,0,0,0);")
        self.pushButton_4.setText("")
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(570, 270, 31, 21))
        self.pushButton_6.setStyleSheet("border-image: url(:/新前缀/1x/1x/资源 4.png);\n"
                                        "background-color: rgba(0,0,0,0);")
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 170, 111, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                                 "color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 260, 121, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                                   "color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "登录"))
        self.pushButton.setText(_translate("MainWindow", "登 录"))
        self.pushButton_2.setText(_translate("MainWindow", "忘记密码"))
        self.pushButton_3.setText(_translate("MainWindow", "注册账号"))
        self.label.setText(_translate("MainWindow", "  用户："))
        self.label_2.setText(_translate("MainWindow", "  密码："))
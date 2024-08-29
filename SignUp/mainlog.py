"""
mainlog.py用于组织登录，注册，密码找回三个页面（加载并持有其ui，并组织页面逻辑）
"""
import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic


class MainLogUi:
    """
    登录界面类，包括self.mainUi, self.passwordFindBackUi, self.signUpUi三个界面
    """

    def __init__(self, path=""):
        # 相对路径
        self.path = path
        # 登录，找回密码，注册三个界面
        self.mainUi, self.passwordFindBackUi, self.signUpUi = self.initUi()

    # 加载三个ui并连接按钮
    def initUi(self):
        # 导入三个ui
        main = uic.loadUi(self.path + "denglu.ui")
        passwordFindBack = uic.loadUi(self.path + "zhaohui.ui")
        signUp = uic.loadUi(self.path + "zhuce.ui")

        # 重设登录界面大小
        rect = QDesktopWidget().availableGeometry().getRect()
        # print(rect) # rect的0,1为左上角坐标(0,0)，2,3为桌面尺寸
        rr = [rect[2], rect[3], int(rect[2] / 10), int(rect[2] / 10) + 30]  # 计算登录页面坐标和大小
        main.setFixedSize(int(rr[0] / 2), int(rr[1] / 2))

        # 为三个界面的按钮连接功能
        # main.pushButton.clicked.connect(self.signInTest) # 这一功能被放到main.py里面了
        main.pushButton_2.clicked.connect(self.openPasswordFindBackUi)
        main.pushButton_3.clicked.connect(self.openSignUpUi)

        passwordFindBack.pushButton_2.clicked.connect(self.openMainUi)
        passwordFindBack.pushButton.clicked.connect(self.findBackPassword)

        signUp.pushButton.clicked.connect(self.signUp)
        signUp.pushButton_2.clicked.connect(self.openMainUi)

        return main, passwordFindBack, signUp

    def openMainUi(self):
        self.signUpUi.close()
        self.signUpUi.lineEdit.clear()
        self.signUpUi.lineEdit_2.clear()
        self.signUpUi.lineEdit_3.clear()
        self.signUpUi.lineEdit_4.clear()

        self.passwordFindBackUi.close()
        self.passwordFindBackUi.lineEdit.clear()
        self.passwordFindBackUi.lineEdit_2.clear()
        self.passwordFindBackUi.lineEdit_5.clear()
        self.passwordFindBackUi.lineEdit_4.clear()

        self.mainUi.show()

    def openPasswordFindBackUi(self):
        self.mainUi.close()
        self.mainUi.lineEdit_2.clear()
        self.mainUi.lineEdit_3.clear()
        self.passwordFindBackUi.show()

    def openSignUpUi(self):
        self.mainUi.close()
        self.mainUi.lineEdit_2.clear()
        self.mainUi.lineEdit_3.clear()
        self.signUpUi.show()

    def findBackPassword(self):
        user_id = self.passwordFindBackUi.lineEdit.text()  # 获取账号
        phonenum = self.passwordFindBackUi.lineEdit_2.text()  # 获取手机号
        password2 = self.passwordFindBackUi.lineEdit_4.text()  # 获取密码
        confirm = self.passwordFindBackUi.lineEdit_5.text()  # 确认密码
        # connect database
        sql = sqlite3.connect("data/user_data.db")
        c = sql.cursor()

        sql1 = '''SELECT name from users where (name=:name)'''
        c.execute(sql1, {'name': user_id})
        flag2 = c.fetchone()
        sql2 = '''SELECT number from users where (number=:number)'''
        c.execute(sql2, {'number': phonenum})
        flag1 = c.fetchone()

        if not flag1:
            QMessageBox.information(None, "提示", "该手机号码不存在！", QMessageBox.Ok)
        elif not flag2:
            QMessageBox.information(None, "提示", "该用户名不存在！", QMessageBox.Ok)
        elif password2 != confirm:
            QMessageBox.information(None, "提示", "两次密码不一致！", QMessageBox.Ok)
        else:
            order1 = '''update users set password=? where name=?'''
            coon = (password2, user_id)
            c.execute(order1, coon)
            QMessageBox.information(None, "提示", "密码修改成功！", QMessageBox.Ok)
            self.openMainUi()
        sql.commit()
        sql.close()

    def signInTest(self):
        """用于检测账号密码对应与否"""
        user_id = self.mainUi.lineEdit_3.text()  # 获取账号
        password = self.mainUi.lineEdit_2.text()  # 获取密码
        sql = sqlite3.connect('data/user_data.db')
        c = sql.cursor()
        sql9 = '''SELECT name from users'''
        c.execute(sql9)
        isUsernameFound = 0
        for i in c.execute(sql9):
            if str(i[0]) == user_id:
                isUsernameFound = 1
                break
        if isUsernameFound == 1:
            sql0 = '''SELECT password,name from users where (name=:name)'''
            c.execute(sql0, {'name': user_id})
            flag = c.fetchone()[0]
            if str(password) == str(flag):
                QMessageBox.information(None, "提示", "登录成功！", QMessageBox.Ok)
                self.mainUi.lineEdit_2.clear()
                self.mainUi.lineEdit_3.clear()
                #####################下面是需要转入的界面
                # myApp.Open1()
                # self.mainUi.close()
                return True  # can sign in
            else:
                QMessageBox.information(None, "提示", "密码错误！", QMessageBox.Ok)
        else:
            QMessageBox.information(None, "提示", "账户不存在！", QMessageBox.Ok)
        return False  # can't sign in

    def signUp(self):
        userName = self.signUpUi.lineEdit.text()  # 获取账号
        phonenum = self.signUpUi.lineEdit_2.text()  # 获取手机号
        password = self.signUpUi.lineEdit_3.text()  # 获取密码
        confirm = self.signUpUi.lineEdit_4.text()  # 确认密码
        # 链接数据库
        conn = sqlite3.connect('data/user_data.db')
        c = conn.cursor()

        if password != confirm:
            QMessageBox.information(None, "提示", "两次输入的密码不一致，请重新输入！", QMessageBox.Ok)
            return
        # else
        sql1 = '''SELECT name from users where (name=:name)'''
        c.execute(sql1, {'name': userName})
        isUserExisted = c.fetchone()
        if isUserExisted:
            QMessageBox.information(None, "提示", "账户已存在！", QMessageBox.Ok)
            return
        # else
        sql2 = '''insert into users
                        (name,password,number)
                        values
                        (:user_name, :user_password,:user_phone)
                    '''
        c.execute(sql2, {'user_name': userName, 'user_password': password, 'user_phone': phonenum})
        # 关闭数据库
        conn.commit()
        conn.close()
        QMessageBox.information(None, "提示", "注册成功！", QMessageBox.Ok)
        self.signUpUi.lineEdit.clear()
        self.signUpUi.lineEdit_2.clear()
        self.signUpUi.lineEdit_3.clear()
        self.signUpUi.lineEdit_4.clear()
        self.openMainUi()

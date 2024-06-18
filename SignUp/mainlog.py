import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from .denglu import Ui_MainWindow1
from .zhaohui import Ui_MainWindow2
from .zhuce import Ui_MainWindow3

change_flag = 1


# 登录界面
class MainWindow(QMainWindow, Ui_MainWindow1):

    def __init__(self, path="", parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.path = path

    def getappfunc(self, func):
        self.appfunc = func

    def Open(self):
        self.show()
        register.close()
        wangjimima.close()
        wangjimima.lineEdit.clear()
        wangjimima.lineEdit_2.clear()
        wangjimima.lineEdit_5.clear()
        wangjimima.lineEdit_4.clear()
        register.lineEdit.clear()
        register.lineEdit_2.clear()
        register.lineEdit_3.clear()
        register.lineEdit_4.clear()


    def cutt(self):
        user_id = self.lineEdit_3.text()  # 获取账号
        password = self.lineEdit_2.text()  # 获取密码
        sql = sqlite3.connect(self.path + 'user_data.db')
        c = sql.cursor()
        sql9 = '''SELECT name from users'''
        c.execute(sql9)
        x = 0
        for i in c.execute(sql9):
            if str(i[0]) == user_id:
                x = 1
                break
        if x == 1:
            sql0 = '''SELECT password,name from users where (name=:name)'''
            c.execute(sql0, {'name': user_id})
            flag = c.fetchone()[0]
            if str(password) == str(flag):
                QMessageBox.information(None, "提示", "登录成功！",
                                        QMessageBox.Ok)
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                #####################下面是需要转入的界面
                # myApp.Open1()
                self.appfunc()
                self.close()
            else:
                QMessageBox.information(None, "提示", "密码错误！",
                                        QMessageBox.Ok)
        else:
            QMessageBox.information(None, "提示", "账户不存在！",
                                    QMessageBox.Ok)


# 注册界面
class Register(QMainWindow, Ui_MainWindow3):
    def __init__(self, path="", parent=None):
        super(Register, self).__init__(parent)
        self.setupUi(self)
        self.path = path

    def Open2(self):
        self.show()
        main.close()

    # 查看两次密码是否一致
    def cut(self):
        password1 = self.lineEdit_3.text()  # 获取密码
        confirm = self.lineEdit_4.text()  # 确认密码
        if password1 != confirm:

            QMessageBox.information(None, "提示", "两次输入的密码不一致，请重新输入！",
                                    QMessageBox.Ok)
        else:
            self.cu1()

    # 查看是否存在用户名
    def cu1(self):
        conn = sqlite3.connect(self.path + 'user_data.db')
        c = conn.cursor()
        x = self.lineEdit.text()
        z = 0
        sql1 = '''SELECT name from users where (name=:name)'''
        c.execute(sql1, {'name': x})
        z = c.fetchone()

        conn.commit()
        conn.close()
        if z:
            QMessageBox.information(None, "提示", "账户已存在！",
                                    QMessageBox.Ok)
        else:
            self.cu()

    def cu(self):
        user_id1 = self.lineEdit.text()  # 获取账号
        phonenum1 = self.lineEdit_2.text()  # 获取手机号
        password1 = self.lineEdit_3.text()  # 获取密码
        conn = sqlite3.connect(self.path + 'user_data.db')
        c = conn.cursor()
        sql1 = '''insert into users
                        (name,password,number)
                        values
                        (:user_name, :user_password,:user_phone)
                    '''
        c.execute(sql1, {'user_name': user_id1, 'user_password': password1, 'user_phone': phonenum1})
        conn.commit()
        conn.close()
        QMessageBox.information(None, "提示", "注册成功！",
                                QMessageBox.Ok)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        main.Open()


# 忘记密码界面
class Wangjimima(QMainWindow, Ui_MainWindow2):
    def __init__(self, path="", parent=None):
        super(Wangjimima, self).__init__(parent)
        self.setupUi(self)
        self.path = path

    def Open3(self):
        self.show()
        main.close()

    def ct(self):
        user_id = self.lineEdit.text()  # 获取账号
        phonenum = self.lineEdit_2.text()  # 获取手机号
        sql = sqlite3.connect(self.path + "user_data.db")
        c = sql.cursor()
        flag1 = 0
        flag2 = 0
        sql1 = '''SELECT name from users where (name=:name)'''
        c.execute(sql1, {'name': user_id})
        flag2 = c.fetchone()
        sql2 = '''SELECT number from users where (number=:number)'''
        c.execute(sql2, {'number': phonenum})
        flag1 = c.fetchone()
        sql.commit()
        sql.close()
        if flag1:
            if flag2:
                password2 = self.lineEdit_4.text()  # 获取密码
                confirm = self.lineEdit_5.text()  # 确认密码
                if password2 == confirm:
                    sql = sqlite3.connect("user_data.db")
                    c = sql.cursor()
                    order1 = '''update users set password=? where name=?'''
                    coon = (password2, user_id)
                    c.execute(order1, coon)
                    sql.commit()
                    sql.close()
                    QMessageBox.information(None, "提示", "密码修改成功！",
                                            QMessageBox.Ok)

                    main.Open()
                else:
                    QMessageBox.information(None, "提示", "两次密码不一致！",
                                            QMessageBox.Ok)
            else:
                QMessageBox.information(None, "提示", "该用户名不存在！",
                                        QMessageBox.Ok)
        else:
            QMessageBox.information(None, "提示", "该手机号码不存在！",
                                    QMessageBox.Ok)


def log_init(path=""):
    global main
    main = MainWindow(path)
    global wangjimima
    wangjimima = Wangjimima(path)
    # 实例化注册页面
    global register
    register = Register(path)

    return main, wangjimima, register


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    wangjimima = Wangjimima()
    # 实例化注册页面
    register = Register()

    # 将按钮与页面打开连接起来
    main.pushButton.clicked.connect(main.cutt)
    main.pushButton_2.clicked.connect(wangjimima.Open3)
    main.pushButton_3.clicked.connect(register.Open2)

    wangjimima.pushButton_2.clicked.connect(main.Open)
    wangjimima.pushButton.clicked.connect(wangjimima.ct)

    register.pushButton.clicked.connect(register.cut)
    register.pushButton_2.clicked.connect(main.Open)

    main.show()

    sys.exit(app.exec_())

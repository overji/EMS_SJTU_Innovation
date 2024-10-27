"""
mainui.py用于组织各个子界面
"""
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic
from PyQt5 import pyrcc
from functools import partial

from ChildPages import main_page, network, wind, solar, EV_main, storage_ui, load_main
from APIs import ScreenScale

# 获取工作区屏幕尺寸，效果同原来写的 rect = QDesktopWidget().availableGeometry().getRect()[2:]
rect = ScreenScale.screenApi().get_working_space_scale()  # 自己写的API，避免`QApplication`未创建时无法使用上面那个方式获取屏幕工作区尺寸
rr = [rect[0], rect[1], int(rect[0] / 10)]  # 三个值分别为：工作区宽度; 工作区高度; 左侧菜单栏宽度 (?


########################################################################################################################
# 程序主界面
class MainWindow:
    def __init__(self):
        super().__init__()
        self.ui = self.initMainUi()  # 加载主界面
        self.winList = self.initWinList()  # 加载各个界面
        self.timer = self.initTimer()  # 计时器初始化
        self.initBtn()  # 按钮功能链接

    def initTimer(self):
        mytimer = QTimer(self.ui)
        for win in self.winList:
            mytimer.timeout.connect(win.timerEvent)
        return mytimer

    def initBtn(self):
        # ##################################### 页面切换按钮 #########################################
        # Btn图片设置
        btnImage = ["", "main.png", "web.svg", "wind.svg", "light.svg", "car.svg", "storage.svg", "blank.png"]
        for i in range(1, 8):
            text = f"\"border-image:url(./pictures/button_image/%s)\" %\"{btnImage[i]}\""
            # self.ui.Btn114.setStyleSheet("border-image:url(./pictures/button_image/btnimage[114])")
            eval(f"self.ui.Btn{i}.setStyleSheet(" + text + ")")
        # Btn大小设置
        for i in range(1, 8):
            # self.listbtn.Btn1.setFixedSize(int(rr[1] / 18), int(rr[1] / 18))
            eval("self.ui.Btn%d.setFixedSize(int(rr[1] / 18), int(rr[1] / 18))" % i)
        # Btn功能连接
        for i in range(1, 8):
            btn = getattr(self.ui, f'Btn{i}')  # 等价于btn = self.ui.Btn{i}
            # partial这个语法等价于self.ui.stackedWidget.setCurrentIndex(i-1)
            btn.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex, i - 1))

        # ########################### 关闭按钮、最小化按钮、测试按钮 #####################################
        # 关闭程序按钮
        self.ui.exitBtn.setFixedSize(int(rr[1] / 40), int(rr[1] / 40))
        self.ui.exitBtn.setStyleSheet("font-size:10pt")
        self.ui.exitBtn.clicked.connect(lambda: sys.exit(0))
        # exitbtn.clicked.connect(lambda: self.timer.stop)

        # 最小化程序按钮
        self.ui.minimizeBtn.setFixedSize(int(rr[1] / 40), int(rr[1] / 40))
        self.ui.minimizeBtn.setStyleSheet("font-size:15pt")
        self.ui.minimizeBtn.clicked.connect(self.ui.showMinimized)

        # 测试更改数据的按钮
        self.ui.testBtn.setFixedSize(int(rr[1] / 40), int(rr[1] / 40))
        self.ui.testBtn.setStyleSheet("font-size:10pt")
        self.ui.testBtn.clicked.connect(self.timerChange)

    def timerChange(self):
        """更换计时器状态，用于作槽函数连接到按钮信号"""
        if self.timer.isActive():
            self.timer.stop()
            self.ui.testBtn.setText("T")
        else:
            self.timer.start(5000)
            self.ui.testBtn.setText("P")

    def initWinList(self):
        win = [
            main_page.MainPage("ChildPages/"),
            network.Network_Ui("ChildPages/"),
            wind.Wind_Ui("ChildPages/"),
            solar.Solar_Ui("ChildPages/"),
            EV_main.EV_Ui("ChildPages/"),
            storage_ui.Storage_Ui("ChildPages/"),
            load_main.Load_Ui("ChildPages/")
        ]
        # 放进stackedWidget视图中
        for i in win:
            self.ui.stackedWidget.addWidget(i.ui)

        return win

    def initMainUi(self):
        # 加载ui文件
        mainUi = uic.loadUi("mainUi.ui")
        # 设置主界面视图
        mainUi.setFixedSize(rr[0], rr[1])  # 注意，这里Fixed，是固定大小，setGeometry虽然也可以设置大小和位置，但是可拖动改变
        mainUi.setWindowTitle("风光储充能量管理系统")
        # 消除边框
        mainUi.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
        )
        return mainUi


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # genetic_alg.get_path("template_For_Data_Prediction/")
    # 创建自定义窗口
    w = MainWindow()
    w.ui.show()
    app.exec_()

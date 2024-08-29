"""
mainui.py用于组织各个子界面
"""
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import pyrcc
from functools import partial

from ChildPages import main_page, network, wind, solar, EV_main, storage_ui, load_main
from APIs import ScreenScale

# 仅供展示时显示界面范围
# 获取工作区屏幕尺寸，效果同 rect = QDesktopWidget().availableGeometry().getRect()[2:]
rect = ScreenScale.screenApi().get_working_space_scale()  # 自己写的API，避免`QApplication`未创建时无法使用上面那个方式获取屏幕工作区尺寸
rr = [rect[0], rect[1], int(rect[0] / 10), int(rect[0] / 10) + 30]


# 一个用于展示图片的widget类 # fzz并没有修改，因为觉得麻烦
class sample_screen(QWidget):
    def __init__(self, example_text, color, id):
        super().__init__()
        self.myinit(example_text, color, id)

    # 展示时居中并缩放图片，QImage
    def myIamge(self, text, x, y):
        image1 = QImage(text)
        map = (x, y)
        image2 = image1.scaled(map[0], map[1] - 100)
        return image2
        ############################

    def myinit(self, example_text, color, id):
        image_list = ["image1.jpg",
                      "image1.jpg", "image2.png", "image3.jpg", "image4.png",
                      "image5.png", "image6.jpg", "image7.png", "image8.jpg"]
        # 垂直布局
        self.qvb = QVBoxLayout()

        # #设置字体背景
        # Label1 = QLabel(example_text)
        # Label1.setStyleSheet("background-color:%s;"%color)
        #
        # #self.qvb.addStretch(1)
        # self.qvb.addWidget(Label1)
        # self.qvb.addStretch(1)  #空间按比例分配，这个在Label下面加入，就是Label置顶，如果再在上面加一个，Label就会居中，解除注释以查看效果
        # self.setLayout(self.qvb)

        # 调色板及图片QPalette，QImage，注意，尽量减少在widget类的设置背景中使用在Label中用的setStyleSheet
        # 因为这可能会导致子控件设置背景及颜色困难
        self.pal = QPalette()
        pal_image = self.myIamge("pictures/backimage/%s" % image_list[id], rr[0] - rr[3], rr[1])
        self.pal.setBrush(self.backgroundRole(), QBrush(pal_image))
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)  # 加上这句，要不不知道为啥图片不显示


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
        mytimer.timeout.connect(self.winList[2].wind_change_text)
        mytimer.timeout.connect(self.winList[3].photo_change_text)
        mytimer.timeout.connect(self.winList[4].EV_timerEvent)
        mytimer.timeout.connect(self.winList[5].storage_change_text)
        mytimer.timeout.connect(self.winList[6].Load_timerEvent)
        return mytimer

    def initBtn(self):
        # ##################################### 页面切换按钮 #########################################
        # Btn图片设置
        btnImage = ["", "main.png", "web.svg", "wind.svg", "light.svg", "car.svg", "storage.svg", "blank.png"]
        for i in range(1, 8):
            text = f"\"border-image:url(./pictures/button_image/%s)\" %\"{btnImage[i]}\""
            # print(text)
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
        if self.timer.isActive():
            self.timer.stop()
            self.ui.testBtn.setText("T")
        else:
            self.timer.start(1000)
            self.ui.testBtn.setText("P")

    def initWinList(self):
        win = [
            main_page.main_page_Ui("ChildPages/", (rr[0] - rr[3], rr[1])),
            network.Network_Ui("ChildPages/"),
            wind.Wind_Ui("ChildPages/"),
            solar.Solar_Ui("ChildPages/"),
            EV_main.EV_Ui("ChildPages/"),
            storage_ui.Storage_Ui("ChildPages/"),
            load_main.Load_Ui("ChildPages/")
        ]
        self.ui.stackedWidget.addWidget(win[0])
        self.ui.stackedWidget.addWidget(win[1].ui)
        self.ui.stackedWidget.addWidget(win[2].ui)
        self.ui.stackedWidget.addWidget(win[3].ui)
        self.ui.stackedWidget.addWidget(win[4].ui)
        self.ui.stackedWidget.addWidget(win[5].ui)
        self.ui.stackedWidget.addWidget(win[6].ui)
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

import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from Storage_System.storage_ui import *
from Wind_System.wind import *
from Solar_System.solar import *
from EV_System.EV_main import *
from Load_System.load_main import *

# 仅供展示时显示界面范围
image_list = ["image1.jpg",
              "image1.jpg", "image2.png", "image3.jpg", "image4.png",
              "image5.png", "image6.jpg", "image7.png", "image8.jpg"]

# 分辨率参数 width,height,左侧宽度，右侧用于减去的宽度（左侧加30，也可以是20或50之类的）
rr = [1440, 900, 150, 150 + 30]


# //////////////////////
# 映射函数，用于展示时缩放图片
# 短边适应
def mymap_short(a, b, c, d):
    x = int(a * max(c / a, d / b))
    y = int(b * max(c / a, d / b))
    return (x, y)


# 长边适应
def mymap_long(a, b, c, d):
    x = int(a * min(c / a, d / b))
    y = int(b * min(c / a, d / b))
    return (x, y)


# 展示时居中并缩放图片，QImage
def myIamge(text, x, y):
    image1 = QImage(text)
    map = (x, y)
    # map = mymap_long(image1.width(), image1.height(), x, y)
    image2 = image1.scaled(map[0], map[1] - 100)
    # l1 = [(map[0]-x)/2,map[0]-(map[0]-x)/2,(map[1]-y)/2,map[1]-(map[1]-y)/2]
    # image2 = image2.copy(int(l1[0]),int(l1[2]),x,y)
    return image2


# 一个具体的右侧widget，用于展示
class sample_screen(QWidget):
    def __init__(self, example_text, color, id):
        super().__init__()
        self.myinit(example_text, color, id)

    def myinit(self, example_text, color, id):
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
        pal_image = myIamge("pictures/backimage/%s" % image_list[id], rr[0] - rr[3], rr[1])
        self.pal.setBrush(self.backgroundRole(), QBrush(pal_image))
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)  # 加上这句，要不不知道为啥图片不显示


# 退出程序
def exitwin():
    sys.exit(0)


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_stacked_layout()  # 多个页面只展示其中一个
        self.create_list_layout()  # 按钮用的
        self.init_ui()

    # 多页面的视图
    def create_stacked_layout(self):
        self.main_screen = QStackedLayout()

        # 页面Widget
        self.win1 = sample_screen("NONE", "gold", 1)
        self.win2 = sample_screen("网络界面", "red", 2)
        self.win3 = Wind_Ui("Wind_System/")
        self.win4 = Solar_Ui("Solar_System/")
        self.win5 = EV_Ui("EV_System/")
        self.win6 = Storage_Ui("Storage_System/")
        self.win7 = Load_Ui("Load_System/")

        # for i in range (1,8):
        #     eval("self.main_screen.addWidget(self.win%d.ui)"%i)

        self.main_screen.addWidget(self.win1)
        self.main_screen.addWidget(self.win2)
        self.main_screen.addWidget(self.win3.ui)
        self.main_screen.addWidget(self.win4.ui)
        self.main_screen.addWidget(self.win5.ui)
        self.main_screen.addWidget(self.win6.ui)
        self.main_screen.addWidget(self.win7.ui)

    # 左侧按钮列表视图
    def create_list_layout(self):
        self.listbtn = uic.loadUi("mainmenu.ui")
        self.listbtn.setLayout(self.listbtn.layout1)

        btnpng = ["", "main.png", "web.svg", "wind.svg", "light.svg", "car.svg", "storage.svg", "blank.png"]

        # 左侧btn图片
        for i in range(1, 8):
            text = "\"border-image:url(./pictures/button_image/%s)\" %\"" + btnpng[i] + "\""
            # print(text)
            eval("self.listbtn.Btn" + str(i) + ".setStyleSheet(" + text + ")")

        # 左侧btn大小
        for i in range(1, 8):
            eval("self.listbtn.Btn%d.setFixedSize(int(rr[1] / 18), int(rr[1] / 18))" % i)

        # 左侧btn连接
        for i in range(1, 8):
            eval("self.listbtn.Btn%d.clicked.connect(self.btn_click%d)" % (i, i))

        self.listbutton = QHBoxLayout()
        self.listbutton.addStretch(1)
        self.listbutton.addWidget(self.listbtn)
        self.listbutton.addStretch(1)

    def init_ui(self):

        # 设置主界面视图
        # 注意，这里Fixed，是固定大小
        # setGoemetry可以设置大小和位置，但是可拖动改变
        self.setFixedSize(rr[0], rr[1])
        self.setWindowTitle("风光储充能量管理系统")

        # 消除边框
        self.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
        )

        # 总体上是水平视图，左侧按钮，右边页面
        container = QHBoxLayout()

        # 创建widget放按钮列表视图
        list_widget = QWidget()
        list_widget.setFixedSize(rr[2], rr[1])
        list_widget.setLayout(self.listbutton)

        # 创建widget放置多页面视图
        main_widget = QWidget()
        main_widget.setLayout(self.main_screen)
        main_widget.setFixedSize(rr[0] - rr[3], rr[1] - int(rr[1] / 20))

        # 水平视图（container）放置这两个widget
        container.addWidget(list_widget)
        container.addWidget(main_widget)

        # 将container应用于主widget
        self.setLayout(container)

        # 设置主widget底色 （#66ccff）,注意用QPalette，要不按钮和其他控件颜色可能会出问题
        pal = QPalette()

        lg = QRadialGradient(rr[0] // 2, rr[1] // 2, int(rr[1] / 1.5), rr[0] // 2, rr[1] // 2)
        lg.setSpread(QRadialGradient.PadSpread)
        lg.setColorAt(0.153409, QColor(39, 98, 216, 255))
        lg.setColorAt(0.8, QColor(16, 16, 181, 255))

        # stop:0.1875 rgba(27, 91, 220, 255), stop:0.607955 rgba(, 255))
        # pal.setBrush(self.backgroundRole(),QColor(16, 16, 181))
        mybrush = QBrush(lg)
        pal.setBrush(self.backgroundRole(), mybrush)
        self.setPalette(pal)

        # 一个退出程序按钮
        exitbtn = QPushButton("X", self)
        exitbtn.setGeometry(rr[0] - int(rr[1] / 40), 0, int(rr[1] / 40), int(rr[1] / 40))
        exitbtn.setStyleSheet("font-size:10pt")
        exitbtn.clicked.connect(exitwin)

        # Minimized
        Miniwin_btn = QPushButton("-", self);
        Miniwin_btn.setGeometry(rr[0] - int(rr[1] / 40) - int(rr[1] / 50 * 1.2), 0, int(rr[1] / 40), int(rr[1] / 40))
        Miniwin_btn.setStyleSheet("font-size:15pt")
        Miniwin_btn.clicked.connect(self.showMinimized)
        # 一个测试更改数据的按钮
        text_change_btn = QPushButton("C", self)
        text_change_btn.setGeometry(int(rr[1] / 50 * 1.2) * 2, 0, int(rr[1] / 40), int(rr[1] / 40))
        text_change_btn.setStyleSheet("font-size:10pt")
        text_change_btn.clicked.connect(self.win6.storage_change_text)
        text_change_btn.clicked.connect(self.win3.wind_change_text)
        text_change_btn.clicked.connect(self.win4.photo_change_text)
        text_change_btn.clicked.connect(self.win5.EV_timerEvent)
        text_change_btn.clicked.connect(self.win7.Load_timerEvent)
        # text_change_btn.clicked.connect(self.win6.storage_change_text) 添加你的函数

        # mytimer
        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.win6.storage_change_text)
        self.mytimer.timeout.connect(self.win3.wind_change_text)
        self.mytimer.timeout.connect(self.win4.photo_change_text)
        self.mytimer.timeout.connect(self.win5.EV_timerEvent)
        self.mytimer.timeout.connect(self.win7.Load_timerEvent)
        # 一个用于测试QTimer的按钮
        self.timer_btn = QPushButton("T", self)
        self.timer_btn.setGeometry(int(rr[1] / 50 * 1.2) * 3, 0, int(rr[1] / 40), int(rr[1] / 40))
        self.timer_btn.setStyleSheet("font-size:10pt")
        self.timer_btn.clicked.connect(self.timer_start)

    def timer_start(self):
        self.mytimer.start(100)
        self.timer_btn.clicked.disconnect(self.timer_start)
        self.timer_btn.clicked.connect(self.timer_stop)
        self.timer_btn.setText("P")

    def timer_stop(self):
        self.mytimer.stop()
        self.timer_btn.clicked.disconnect(self.timer_stop)
        self.timer_btn.clicked.connect(self.timer_start)
        self.timer_btn.setText("T")

    # 以下均为按钮触发事件,用于页面切换
    # 页面的编号是按照添加顺序的前后去定的
    def btn_click1(self):
        self.main_screen.setCurrentIndex(0)

    def btn_click2(self):
        self.main_screen.setCurrentIndex(1)

    def btn_click3(self):
        self.main_screen.setCurrentIndex(2)

    def btn_click4(self):
        self.main_screen.setCurrentIndex(3)

    def btn_click5(self):
        self.main_screen.setCurrentIndex(4)

    def btn_click6(self):
        self.main_screen.setCurrentIndex(5)

    def btn_click7(self):
        self.main_screen.setCurrentIndex(6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rect = QDesktopWidget().availableGeometry().getRect()
    print(rect)
    rr[0] = rect[2]
    rr[1] = rect[3]
    rr[2] = int(rr[0] / 10)
    rr[3] = rr[2] + 30
    # 创建自定义窗口
    w = MyWindow()
    w.show()
    app.exec_()

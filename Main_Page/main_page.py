from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime
import ctypes
import sqlite3
import pandas as pd
from Main_Page.fetch_weather_info import *
class main_page_Ui(QWidget):
    path = None
    def __init__(self, relative_path="",Map=(1000,1000)):
        super().__init__()

        self.Map = Map
        self.path = relative_path
        self.ui = uic.loadUi(self.path + "MainPage.ui")
        #self.ui.setLayout(self.ui.layout)
        text = "\"border-image:url(./pictures/white.png)\""
        for i in range(1,6):
            eval("self.ui.Btn_"+str(i)+".setStyleSheet("+text+")")

        self.ui.Btn_1.clicked.connect(self.Btn_1_click)
        self.ui.Btn_2.clicked.connect(self.Btn_2_click)
        self.ui.Btn_3.clicked.connect(self.Btn_3_click)
        self.ui.Btn_4.clicked.connect(self.Btn_4_click)
        self.ui.Btn_5.clicked.connect(self.Btn_5_click)

        self.myinit()
        self.updateDate()
        self.updateWeather()

    def updateDate(self):
        current_datetime = QDateTime.currentDateTime()
        date = current_datetime.date()
        year = date.year()
        month = date.month()
        day = date.day()
        self.ui.label_5.setText(f"{year}/{month}/{day}")

    def updateWeather(self):
        temperature,wind = get_weather()
        self.ui.label_7.setText(wind)
        self.ui.label_9.setText(temperature)

    def Btn_1_click(self):
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        df_EV = df["BatteryChange"]
        text = "电动汽车充电桩\n运行功率：%.2f" % (df_EV[2]) + " kWh"
        self.ui.label_16.setText(text)

    def Btn_2_click(self):
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        df_WIND = df["windkW"]
        text = "风机\n运行功率：%.2f" % (df_WIND[1]) + " kWh"
        self.ui.label_16.setText(text)

    def Btn_3_click(self):
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        df_ = df["loadkW"]
        text = "负荷\n运行功率：%.2f" % (df_[1]) + " kWh"
        self.ui.label_16.setText(text)

    def Btn_4_click(self):
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        df_ = df["BatteryChange"]
        text = "储能\n运行功率：%.2f" % (df_[6]) + " kWh"
        self.ui.label_16.setText(text)

    def Btn_5_click(self):
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        df_ = df["BatteryChange"]
        text = "光伏\n运行功率：%.2f" % (df_[3]) + " kWh"
        self.ui.label_16.setText(text)

    def setstylesheet(self):
        standard_font_size = 15
        standard_dpi = 96 * 1.75
        current_dpi = ctypes.windll.user32.GetDpiForWindow(ctypes.windll.user32.GetDesktopWindow())
        font_size = standard_font_size * (current_dpi / standard_dpi)
        stylesheet = f"""
                font-family:Microsoft YaHei;
                font-size:{font_size}pt;
                padding:10px;
            """
        self.setStyleSheet(stylesheet)

    def myinit(self):
        self.QHB=QHBoxLayout()
        self.PHOTO = QWidget()
        self.PHOTO.setFixedSize(self.Map[0]//3*2,self.Map[1])
        self.pal = QPalette()
        pal_image = self.myIamge("pictures/backimage/image1.jpg", self.Map[0]//3*2, self.Map[1])  # rr[0] - rr[3], rr[1]
        self.pal.setBrush(self.PHOTO.backgroundRole(), QBrush(pal_image))
        self.PHOTO.setPalette(self.pal)
        self.PHOTO.setAutoFillBackground(True)  # 加上这句，要不不知道为啥图片不显示
        self.PHOTO.setLayout(self.ui.MainPageLayout)


        self.LIST = QWidget()
        self.LIST.setFixedSize(int(self.Map[0]/3.1),self.Map[1])
        self.LIST.setLayout(self.ui.MainDetailLayout)
        self.QHB.addWidget(self.PHOTO)
        self.QHB.addWidget(self.LIST)
        self.setLayout(self.QHB)


    def myIamge(self,text, x, y):
        image1 = QImage(text)
        map = (x, y)
        # map = mymap_long(image1.width(), image1.height(), x, y)
        image2 = image1.scaled(map[0], map[1] - 100)
        # l1 = [(map[0]-x)/2,map[0]-(map[0]-x)/2,(map[1]-y)/2,map[1]-(map[1]-y)/2]
        # image2 = image2.copy(int(l1[0]),int(l1[2]),x,y)
        return image2





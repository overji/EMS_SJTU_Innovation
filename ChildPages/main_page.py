import random

from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime
import ctypes
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

from APIs.fetch_weather_info import get_weather
from .ChildPageBase import ChildPage


class MainPage(ChildPage):

    def __init__(self, relative_path=""):
        super().__init__(relative_path, "MainPage.ui")
        # 重写后的函数会在super().__init__()中执行

    def initUi(self):
        # ######################################## 加载主界面图 ########################################
        backImagePath = "./pictures/backimage/image1.jpg"  # 绝对路径 相对于mainui.py
        self.ui.mainPhotoWidget.setStyleSheet(
            "#mainPhotoWidget {border-image: url(" + backImagePath + ");}")
        # ######################################## 加载日期信息 ########################################
        date = QDateTime.currentDateTime().date()
        self.ui.label_5.setText(f"{date.year()}/{date.month()}/{date.day()}")
        # ######################################## 加载天气信息 ########################################
        temperature, wind = get_weather()
        self.ui.label_7.setText(wind)
        self.ui.label_9.setText(temperature)

    def initButton(self):
        # 设置按钮背景 (透明)
        text = "\"border-image:url(./pictures/white.png)\""
        for i in range(1, 6):
            eval("self.ui.Btn_" + str(i) + ".setStyleSheet(" + text + ")")

        # 连接槽函数
        self.ui.Btn_1.clicked.connect(lambda: self.btnClicked("BatteryChange", "电动汽车充电桩"))
        self.ui.Btn_2.clicked.connect(lambda: self.btnClicked("windkW", "风机"))
        self.ui.Btn_3.clicked.connect(lambda: self.btnClicked("loadkW", "负荷"))
        self.ui.Btn_4.clicked.connect(lambda: self.btnClicked("BatteryChange", "储能"))
        self.ui.Btn_5.clicked.connect(lambda: self.btnClicked("BatteryChange", "光伏"))

    def btnClicked(self, col_of_db="", title=""):
        engine = create_engine('mysql+mysqlconnector://EMS:282432@112.124.43.86/ems')

        query = "SELECT * FROM EMS_Data"
        df = pd.read_sql(query, engine)
        df_col = df[col_of_db]
        text = title + "\n运行功率：%.2f" % (df_col[random.randint(0, 9)]) + " kWh"  # random只是为了看起来随机一点实际上没有任何作用
        self.ui.label_16.setText(text)

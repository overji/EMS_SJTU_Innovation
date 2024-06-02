from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import pandas as pd
import sqlite3
from matplotlib import pyplot as plt
import ctypes


class Wind_Ui():
    path = ""

    def __init__(self, relative_path=""):
        Wind_Ui.path = relative_path
        self.ui = uic.loadUi(self.path + "wind.ui")
        self.ui.setLayout(self.ui.verticalLayout)
        self.summon_pic1()
        # set style sheet
        self.setstylesheet()

    def setstylesheet(self):
        standard_font_size = 14
        standard_dpi = 96 * 1.75
        current_dpi = ctypes.windll.user32.GetDpiForWindow(ctypes.windll.user32.GetDesktopWindow())
        font_size = standard_font_size * (current_dpi / standard_dpi)
        stylesheet = f"""
                font-family:Microsoft YaHei;
                font-size:{font_size}pt;
                padding:10px;
            """
        self.ui.setStyleSheet(stylesheet)

    def wind_change_text(self):
        # 这里更新图像和label的数据
        self.summon_pic1()
        # self.summon_pic2()
        picmap1 = QPixmap(self.path + "pictures/wind_pic1.jpg")
        self.ui.pic_1.setPixmap(picmap1)
        self.ui.pic_1.setScaledContents(True)
        # picmap2 = QPixmap(self.path + "pictures/wind_pic2.jpg")
        # self.ui.pic_2.setPixmap(picmap2)
        # self.ui.pic_2.setScaledContents(True)
        self.read_data_to_text()
        # self.old_wind_change_text()

    def read_data_to_text(self):
        # 从数据库里面读取数据，并且写入Label中
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        data_column = df["time"]
        windkW = df["windkW"]
        self.ui.data5.setText(f"{windkW[int(time.time() * 10) % 60]}")
        data = [0, 16337.2, 15.14, 447.85, 318.1, 0, 40.6 * 140 + 13.53, 15, 40.1, 18, 1533.1, 381, 16337.2, 19, 5317.6,
                0, 0, 0]
        for i in range(1, 16):
            if (i == 5):
                continue
            elif (i == 15):
                self.ui.data15.setText("CC")
                continue
            eval(f"self.ui.data{i}.setText(\"{data[i]}\")")

    def summon_pic1(self):
        # 从数据库里面读取数据，生成图片
        fig, ax = plt.subplots(figsize=(4.58, 3.87))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        dt = int(time.time() * 10 % 60)
        ax.plot(df["windkW"][0 + dt:60 + dt])
        ax.set_title("Wind Power")
        ax.set_xlabel("t(s)")
        ax.set_ylabel("power(kW)")
        plt.savefig(self.path + "pictures/wind_pic1.jpg")
        plt.close()

    def summon_pic2(self):
        # 从数据库里面读取数据，生成图片
        fig, ax = plt.subplots(figsize=(6.28, 5.52))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        dt = int(time.time() * 10 % 60)
        ax.plot(df["sell_price"][0 + dt:60 + dt])
        ax.set_title("Sell Price")
        ax.set_xlabel("t(s)")
        ax.set_ylabel("price(CNY) ")
        plt.savefig(self.path + "pictures/wind_pic2.jpg")
        plt.close()

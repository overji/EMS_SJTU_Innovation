import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


class Solar_Ui():
    path = None

    def __init__(self, relative_path=None):
        Solar_Ui.path = relative_path
        self.ui = uic.loadUi(self.path + "solar.ui")
        self.ui.setLayout(self.ui.verticalLayout)
        self.summon_pic1()
        self.summon_pic2()

    def photo_change_text(self):
        # 这里更新图像和label的数据
        self.summon_pic1()
        self.summon_pic2()
        picmap1 = QPixmap(self.path + "pictures/photo_pic1.jpg")
        self.ui.pic_1.setPixmap(picmap1)
        self.ui.pic_1.setScaledContents(True)
        # picmap2 = QPixmap(self.path + "pictures/photo_pic2.jpg")
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
        photokW = df["photokW"]
        self.ui.data5.setText(f"{photokW[int(time.time() * 10) % 60]}")
        data = [0, 17835.2, 17.12, 531.74, 393.1, 0, 41.7 * 160 + 17.14, 16, 41.7, 10, 1652.1, 284, 17835.2, 19, 5482.1,
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
        ax.set_title("Photo Power")
        ax.set_xlabel("t(s)")
        ax.set_ylabel("power(kW)")
        ax.plot(df["photokW"][0 + dt:60 + dt])
        plt.savefig(self.path + "pictures/photo_pic1.jpg")
        plt.close()

    def summon_pic2(self):
        # 从数据库里面读取数据，生成图片
        fig, ax = plt.subplots(figsize=(6.28, 5.52))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        dt = int(time.time() * 10 % 60)
        ax.plot(df["sell_price"][0 + dt:60 + dt])
        ax.set_xlabel("t(h)")
        ax.set_ylabel("price(CNY)")
        plt.savefig(self.path + "pictures/photo_pic2.jpg")
        plt.close()

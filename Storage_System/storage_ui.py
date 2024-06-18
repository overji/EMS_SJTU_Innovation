import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
import ctypes

class Storage_Ui():
    path = None
    get_data = None
    def __init__(self, relative_path=None,relative_data=None):
        Storage_Ui.path = relative_path
        self.get_data = relative_data
        self.ui = uic.loadUi(self.path + "storage.ui")
        self.ui.setLayout(self.ui.layout1)
        self.list1 = [0 for i in range(60)]
        self.t = int(time.time() * 10) % 90
        self.setstylesheet()
        self.ui.pushButton.setStyleSheet("border-image:url(./pictures/white.png);color: rgb(255, 255, 255);")
        self.ui.pushButton.clicked.connect(self.btnclick1)
    def old_storage_change_text(self):
        for i in range(1, 19):
            # self.win6.data1.setText("11111")

            str1 = str(i) + "." + "%02d" % (int(time.time() * 10) % 100)  # 时间

            eval("self.ui.data%d.setText(\"%s\")" % (i, str1))

            # print(i)

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
        self.ui.setStyleSheet(stylesheet)

    def storage_change_text_1(self):
        self.t = int(time.time() * 10) % 90
        self.pic1()
        image = QImage(self.path + "pictures/storage_pic1.jpg")
        image.scaled(self.ui.PHOTO.size())
        spic1 = QPixmap(image)
        self.ui.PHOTO.setPixmap(spic1)
        self.ui.PHOTO.setScaledContents(True)
        self.read_data_to_text()

    def storage_change_text_2(self):
        self.pic2()
        self.pic1()
        image = QImage(self.path + "pictures/storage_pic2.jpg")
        image.scaled(self.ui.PHOTO.size())
        spic2 = QPixmap(image)
        self.ui.PHOTO.setPixmap(spic2)
        self.ui.PHOTO.setScaledContents(True)
        #self.read_data_to_text()

    def storage_change_text(self):
        self.storage_change_text_2()

    def pic2(self):
        fig, ax = plt.subplots(figsize=(5.0, 3.87))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT BatteryChange FROM dataTable"  # 假设汽车的调度数据在CarChange列
        df = pd.read_sql_query(query, conn)
        ax.set_xlabel("time(h)")
        ax.set_ylabel("Energy(kW)")
        ax.set_title("Storage_system")
        ax.bar([i for i in range(0, 24)], df["BatteryChange"][0:24], color='g', label='Battery')  # 电池的调度数据用蓝色表示
        ax.legend()  # 显示图例
        plt.savefig(self.path + "pictures/storage_pic2.jpg")
        plt.close()

    def pic1(self):
        fig, ax = plt.subplots(figsize=(5.0, 3.87))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT x_values FROM dataTable"
        df = pd.read_sql_query(query, conn)
        ax.set_xlabel("times")
        ax.set_ylabel("Total cost ratio")
        ax.set_title("Fit value")
        size = (df["x_values"].shape)[0]
        print(df["x_values"])
        ax.plot([i for i in range(0, size)],
                (df["x_values"] - df["x_values"].min()) / (df["x_values"].max() - df["x_values"].min()))
        plt.savefig(self.path + "pictures/storage_pic1.jpg")
        plt.close()

    def read_data_to_text(self):
        b = min(max(self.t, 15), 45) - 15
        a = self.t - b
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        data_column = [0, 500.90, 2.30, 00.00, 100.00, 100.00, 30, 530.65, 229.65, 0.65, 3.00, 1.00, 30, 2.34, 2.26,
                       26.5, 24.00, 99, 97]

        self.ui.data3.setText("%.2f" % self.list1[a])
        self.ui.data2.setText("%.2f" % (self.list1[a] / 2))
        for i in range(1, 19):
            if i == 3 or i == 2: continue
            eval("self.ui.data%d.setText(\"%.2f\")" % (i, data_column[i]))

    def btnclick1(self):
        self.ui.pushButton.clicked.connect(self.btnclick2)
        self.ui.pushButton.clicked.disconnect(self.btnclick1)
        self.storage_change_text_2()
    def btnclick2(self):
        self.ui.pushButton.clicked.connect(self.btnclick1)
        self.ui.pushButton.clicked.disconnect(self.btnclick2)
        self.storage_change_text_1()
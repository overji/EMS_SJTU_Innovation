"""
# 控件命名：
# 左侧：
## 实时负荷数据：ld_lb_dt_1~7
# 右侧：
## 曲线图：pw_fg
## 调控按钮：set_btn_1~3
"""
import sys
import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import pandas as pd
import sqlite3
from matplotlib import pyplot as plt
import ctypes


class Load_Ui():
    path = None

    def __init__(self, relative_path=""):
        Load_Ui.path = relative_path
        self.ui = uic.loadUi(self.path + "load.ui")  # 加载ui文件
        self.ui.setLayout(self.ui.mainLayout)  # 设置界面主布局为主布局total_layout
        self.connect_button_func()  # 连接按钮信号与函数
        self.setstylesheet()

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

    def Load_timerEvent(self):
        self.t = int(time.time() * 10) % 90
        self.Load_data_update()
        self.Load_graph_update()

    # 更新数据显示
    def Load_data_update(self):
        """更新数据显示"""
        # 读取数据库对象，为df
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        # 获取df的各列数据
        df_time = df["time"]
        windkW = df["windkW"]
        loadkW = df["loadkW"]
        photokW = df["photokW"]
        sell_price = df["sell_price"]
        buy_price = df["buy_price"]
        current_situation = df["current_situation"]
        # 设置数据
        self.ui.ld_lb_dt_1.setText(f"{windkW[int(time.time() * 10) % 60]}")
        self.ui.ld_lb_dt_2.setText(f"{windkW[int(time.time() * 10) % 60]}")
        self.ui.ld_lb_dt_3.setText(f"{loadkW[int(time.time() * 10) % 60]}")
        self.ui.ld_lb_dt_4.setText(f"{photokW[int(time.time() * 10) % 60]}")
        self.ui.ld_lb_dt_5.setText(f"{sell_price[int(time.time() * 10) % 60]}")
        self.ui.ld_lb_dt_6.setText(f"{buy_price[int(time.time() * 10) % 60]}")
        self.ui.ld_lb_dt_7.setText(f"{current_situation[int(time.time() * 10) % 60]}")

    # 更新曲线图
    def Load_graph_update(self):
        """更新曲线图"""
        fig, ax = plt.subplots(figsize=(6.28, 5.52))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        ax.set_xlabel("t(s)")
        ax.set_ylabel("Power(kw)")
        ax.set_title("load Power")
        a = min(max(self.t, 15), 45) - 15
        ax.plot(df["loadkW"][0 + a:60 + a])
        tmp = df["loadkW"]
        ax.plot([self.t], tmp[self.t], color="red", marker="o")
        plt.savefig(self.path + "pictures/loadkW.jpg")
        plt.close()
        # 以上绘制图片并保存，以下更新界面
        picmap1 = QPixmap(self.path + "pictures/loadkW.jpg")
        self.ui.pw_fg.setPixmap(picmap1)
        self.ui.pw_fg.setScaledContents(True)

    # 连接按钮信号与函数
    def connect_button_func(self):
        """连接按钮信号与函数"""
        # 初始化控制按钮1（更新数据）
        self.ui.set_btn_1.clicked.connect(self.Load_data_update)
        # 初始化控制按钮2（更新曲线图）
        self.ui.set_btn_2.clicked.connect(self.Load_graph_update)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_ui = Load_UI()
    load_ui.ui.show()
    app.exec_()

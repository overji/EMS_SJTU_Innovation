"""
变量命名：
# 左侧
## 充电桩铭牌参数：ns_lb_dt_1~5
## 充电桩充电情况：pw_lb_dt_1~3
# 右侧
## 图片：pw_fg
## 设置按钮：set_btn_1~3
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


class EV_Ui():
    """调用时请调用EV_Ui().ui"""
    path = None

    def __init__(self, relative_path=""):
        """界面初始化"""
        EV_Ui.path = relative_path
        self.ui = uic.loadUi(self.path + "EV.ui")  # 加载ui文件
        self.ui.setLayout(self.ui.mainLayout)  # 设置界面主布局
        self.connect_button_func()  # 连接按钮信号与函数
        self.t = int(time.time() * 10) % 90

    # 定时触发事件
    def EV_timerEvent(self):
        """定时触发事件"""
        self.EV_data_update()
        self.EV_graph_update()
        self.t = int(time.time() * 10) % 90

    # 更新数据显示
    def EV_data_update(self):
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
        # self.ui.ns_lb_dt_1.setText(f"{windkW[int(time.time() * 10) % 60]}")
        self.ui.ns_lb_dt_2.setText(f"{windkW[int(time.time() * 10) % 60]}")
        self.ui.ns_lb_dt_3.setText(f"{loadkW[int(time.time() * 10) % 60]}")
        self.ui.ns_lb_dt_4.setText(f"{photokW[int(time.time() * 10) % 60]}")
        self.ui.ns_lb_dt_5.setText(f"{sell_price[int(time.time() * 10) % 60]}")
        self.ui.pw_lb_dt_1.setText(f"{buy_price[int(time.time() * 10) % 60]}")
        self.ui.pw_lb_dt_2.setText(f"{current_situation[int(time.time() * 10) % 60]}")
        self.ui.pw_lb_dt_3.setText(f"{df_time[int(time.time() * 10) % 60]}")

    # 更新曲线图
    def EV_graph_update(self):
        """更新曲线图"""
        fig, ax = plt.subplots(figsize=(6.28, 5.52))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        ax.set_xlabel("t(s)")
        ax.set_ylabel("Power(kw)")
        ax.set_title("EV Power")
        a = min(max(self.t, 15), 45) - 15
        ax.plot(df["photokW"][0 + a:60 + a])
        tmp = df["photokW"]
        ax.plot([self.t], tmp[self.t], color="red", marker="o")
        plt.savefig(self.path + "EV_pictures/photokW.jpg")
        plt.close()
        # 以上绘制图片并保存，以下更新界面
        picmap1 = QPixmap(self.path + "EV_pictures/photokW.jpg")
        self.ui.pw_fg.setPixmap(picmap1)
        self.ui.pw_fg.setScaledContents(True)

    # 连接按钮信号与函数
    def connect_button_func(self):
        """连接按钮信号与函数"""
        # 初始化控制按钮1（更新数据）
        self.ui.set_btn_1.clicked.connect(self.EV_data_update)
        # 初始化控制按钮2（更新曲线图）
        self.ui.set_btn_2.clicked.connect(self.EV_graph_update)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = EV_Ui()
    a.ui.show()
    app.exec_()

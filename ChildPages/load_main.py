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

from .ChildPageBase import ChildPage
from APIs.FigureDraw import FigureDraw


class Load_Ui(ChildPage):

    def __init__(self, relative_path=""):
        super().__init__(relative_path, "load.ui")

    def timerEvent(self):
        self.update_label_data()
        self.update_graph()

    # 连接按钮信号与函数
    def initButton(self):
        """连接按钮信号与函数"""
        # 初始化控制按钮1（更新数据）
        self.ui.set_btn_1.clicked.connect(self.update_label_data)
        # 初始化控制按钮2（更新曲线图）
        self.ui.set_btn_2.clicked.connect(self.update_graph)

    # 更新数据显示
    def update_label_data(self):
        """更新数据显示"""
        # 读取数据库对象，为df
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)

        # 获取df的各列数据
        # df_time = df["time"]
        windkW = df["windkW"]
        loadkW = df["loadkW"]
        photokW = df["photokW"]
        sell_price = df["sell_price"]
        buy_price = df["buy_price"]
        current_situation = df["current_situation"]

        # 设置数据
        col_list = [windkW, windkW, loadkW, photokW, sell_price, buy_price, current_situation]
        for i in range(1, 8):
            data_label = getattr(self.ui, f"ld_lb_dt_{i}")
            data_label.setText(f"{(col_list[i - 1])[int(time.time() * 10) % 60]}")  # 关于时间的随机数选取

    # 更新曲线图
    def update_graph(self):
        """更新曲线图"""
        # 绘制图像并保存
        FigureDraw().generate_line_chart_2("loadkW", "load Power", "t(s)", "Power(kw)")
        # 获取图片并填充控件
        backImagePath = "pictures/Figures/load Power.jpg"
        self.ui.pw_fg.setStyleSheet("#pw_fg {border-image: url(" + backImagePath + ");}")


if __name__ == "__main__":
    from ..APIs.FigureDraw import FigureDraw

    app = QApplication(sys.argv)
    load_ui = Load_Ui()
    load_ui.ui.show()
    app.exec_()

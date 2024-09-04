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
import ctypes
from matplotlib import pyplot as plt

from .ChildPageBase import ChildPage
from APIs.FigureDraw import FigureDraw


class EV_Ui(ChildPage):

    def __init__(self, relative_path=""):
        super().__init__(relative_path, "EV.ui")

    # 定时触发事件
    def timerEvent(self):
        """定时触发事件"""
        self.EV_data_update()
        self.EV_graph_update()

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
        # 绘制图像并保存
        FigureDraw().generate_bar_graph_1("BatteryChange", "EV_System", "time(h)", "Energy(kW)", bar_color='r')
        # FigureDraw().generate_line_chart_2("BatteryChange", "EV_System", "time(h)", "Energy(kW)")
        # 获取图片并填充控件
        backImagePath = "pictures/Figures/EV_System.jpg"
        self.ui.pw_fg.setStyleSheet("#pw_fg {border-image: url(" + backImagePath + ");}")

    # 连接按钮信号与函数
    def initButton(self):
        """连接按钮信号与函数"""
        # 初始化控制按钮1（更新数据）
        self.ui.set_btn_1.clicked.connect(self.EV_data_update)
        # 初始化控制按钮2（更新曲线图）
        self.ui.set_btn_2.clicked.connect(self.EV_graph_update)


if __name__ == "__main__":
    from ..APIs.FigureDraw import FigureDraw

    app = QApplication(sys.argv)
    a = EV_Ui()
    a.ui.show()
    app.exec_()

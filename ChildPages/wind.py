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


class Wind_Ui(ChildPage):

    def __init__(self, relative_path=""):
        super().__init__(relative_path, "wind.ui")

    def timerEvent(self):
        self.update_label_data()
        self.update_pic()

    def update_pic(self):
        """更新曲线图"""
        # 绘制图像并保存
        FigureDraw().generate_line_chart_2("windkW", "Wind Power", "t(h)", "power(kW)")
        # 获取图片并填充控件
        backImagePath = "pictures/Figures/Wind Power.jpg"
        self.ui.pic_1.setStyleSheet("#pic_1 {border-image: url(" + backImagePath + ");}")

    def update_label_data(self):
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


if __name__ == "__main__":
    from ..APIs.FigureDraw import FigureDraw

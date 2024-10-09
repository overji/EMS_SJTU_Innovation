import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import time
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import ctypes

from sqlalchemy import create_engine

from .ChildPageBase import ChildPage
from APIs.FigureDraw import FigureDraw


class Solar_Ui(ChildPage):

    def __init__(self, relative_path=""):
        super().__init__(relative_path, "solar.ui")

    def timerEvent(self):
        self.update_pic()
        self.update_label_data()

    def update_pic(self):
        # 绘制图像并保存
        FigureDraw().generate_line_chart_2("photokW", "Photo Power", "t(h)", "power(kW)")
        # 获取图片并填充控件
        backImagePath = "pictures/Figures/Photo Power.jpg"
        self.ui.pic_1.setStyleSheet("#pic_1 {border-image: url(" + backImagePath + ");}")

    def update_label_data(self):
        # 从数据库里面读取数据，并且写入Label中
        engine = create_engine('mysql+mysqlconnector://EMS:282432@112.124.43.86/ems')

        query = "SELECT * FROM EMS_Data"
        df = pd.read_sql(query, engine)
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


if __name__ == "__main__":
    from ..APIs.FigureDraw import FigureDraw

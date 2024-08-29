"""
变量命名：
# 标题：title_lb，小标题label_1~4
# 实时数据监控：rt_hd/dt/un_lb_dt_1~4
# 设备管理按钮：ctl_btn_1~5
# 警报通知：wrn_lb_1
# 能源报告：rpt_hd/dt/un_lb_dt_1~3
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


class Network_Ui():
    """调用时请调用Network_Ui().ui"""
    path = None

    def __init__(self, relative_path=""):
        """界面初始化"""
        Network_Ui.path = relative_path
        self.ui = uic.loadUi(self.path + "network.ui")  # 加载ui文件
        self.ui.setLayout(self.ui.mainLayout)  # 设置界面主布局
        self.connect_button_func()  # 连接按钮信号与函数
        self.t = int(time.time() * 10) % 90
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

    # 定时触发事件
    def Network_timerEvent(self):
        """定时触发事件"""
        self.Network_data_update()
        self.Network_graph_update()
        self.t = int(time.time() * 10) % 90

    # 更新数据显示
    # def Network_data_update(self):
    #     """更新数据显示"""
    #     读取数据库对象，为df
    #     conn = sqlite3.connect("data/data_db.db")
    #     query = "SELECT * FROM dataTable"
    #     df = pd.read_sql_query(query, conn)
    #     获取df的各列数据
    #     df_time = df["time"]
    #     设置数据
    #     self.ui.ns_lb_dt_1.setText(f"{windkW[int(time.time() * 10) % 60]}")

    # 更新曲线图
    # def Network_graph_update(self):
    #     """更新曲线图"""
    #     fig, ax = plt.subplots(figsize=(6.28, 5.52))
    #     conn = sqlite3.connect("data/data_db.db")
    #     query = "SELECT * FROM dataTable"
    #     df = pd.read_sql_query(query, conn)
    #     ax.set_xlabel("t(s)")
    #     ax.set_ylabel("Power(kw)")
    #     ax.set_title("Network Power")
    #     a = min(max(self.t, 15), 45) - 15
    #     ax.plot(df["photokW"][0 + a:60 + a])
    #     tmp = df["photokW"]
    #     ax.plot([self.t], tmp[self.t], color="red", marker="o")
    #     plt.savefig(self.path + "Network_pictures/photokW.jpg")
    #     plt.close()
    #     # 以上绘制图片并保存，以下更新界面
    #     picmap1 = QPixmap(self.path + "Network_pictures/photokW.jpg")
    #     self.ui.pw_fg.setPixmap(picmap1)
    #     self.ui.pw_fg.setScaledContents(True)

    # 连接按钮信号与函数
    def connect_button_func(self):
        """连接按钮信号与函数"""
        # 初始化控制按钮1（更新数据）
        # self.ui.set_btn_1.clicked.connect(self.Network_data_update)
        # 初始化控制按钮2（更新曲线图）
        # self.ui.set_btn_2.clicked.connect(self.Network_graph_update)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Network_Ui()
    a.ui.show()
    app.exec_()

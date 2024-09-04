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

from .ChildPageBase import ChildPage


class Network_Ui(ChildPage):

    def __init__(self, relative_path=""):
        """界面初始化"""
        super().__init__(relative_path, "network.ui")

    # 定时触发事件
    def timerEvent(self):
        pass
        # self.Network_data_update()
        # self.Network_graph_update()

    # 连接按钮信号与函数
    def initButton(self):
        """连接按钮信号与函数"""
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Network_Ui()
    a.ui.show()
    app.exec_()

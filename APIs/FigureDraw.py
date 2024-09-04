import time

import pandas as pd
from matplotlib import pyplot as plt
import sqlite3


# fzz吐槽：从设计模式上来讲这里最规范的写法应该是每多一种绘图格式or风格就新建一个子类继承自FigureDraw基类；但是fzz太懒了
# 于是这里每多一个绘图格式就需要同时建立两个函数，一个作为plot_func用于设计绘图格式，一个用作api接口

class FigureDraw:
    """
    绘图接口类，可用于绘制各种各样的图表
    目前已有绘制标准条形图和标准折线图两种
    针对后期绘图的不同需求，接口可以扩展，私有方法也可以修改
    计划每一种风格的图像就写一个方法
    """

    def __init__(self, db_path="data/data_db.db"):
        self.db_path = db_path

    def __fetch_and_prepare_data(self, col_name, data_range, isNormalized):
        """
        从数据库中获取指定列的数据，并根据范围进行切片和归一化处理。

        参数:
        - col_name: 查询列标题（字符串）
        - data_range: 数据范围（整数二元组）
        - isNormalized: 是否对数据归一化（布尔值）

        返回:
        - 处理后的 pandas.Series 对象。
        """
        # 连接数据库
        conn = sqlite3.connect(self.db_path)
        # 查询数据
        query = f"SELECT {col_name} FROM dataTable"
        df = pd.read_sql_query(query, conn)[col_name]
        # 设定数据范围
        df = df[data_range[0]:data_range[1]]
        # 根据条件归一化数据
        if isNormalized:
            df = (df - df.min()) / (df.max() - df.min())
        return df

    def __create_plot(self, df, x_label, y_label, title, save_path, figsize, plot_func, **plot_kwargs):
        """
        创建并保存图表。（一个上下文环境）

        参数:
        - df: 处理后的数据（pandas.Series 对象）
        - x_label: 横轴标签（字符串）
        - y_label: 纵轴标签（字符串）
        - title: 图表标题（字符串）
        - save_path: 图像保存路径（字符串）
        - figsize: 图像大小（二元组）
        - plot_func: 用于绘制图表的函数，参数为(ax,x_series,y_series,**plot_kwargs)
        - plot_kwargs: 传递给 plot_func 的其他关键字参数

        返回:
        - 无，图像直接保存至指定路径。
        """
        # 创建图形和轴
        fig, ax = plt.subplots(figsize=figsize)
        # 设置图表标签和标题
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        # 绘制图表
        x_series = range(len(df))
        plot_func(ax, x_series, df, **plot_kwargs)

        # 显示图例（如果有）
        if "label" in plot_kwargs:
            ax.legend()

        # 保存图像
        plt.savefig(save_path)
        # 关闭图形
        plt.close()

    # 绘制折线图 1
    def __draw_line_chart(self, ax, x_series, y_series, color="b"):
        """绘制默认为蓝色的折线图"""
        ax.plot(x_series, y_series, color=color)

    def generate_line_chart_1(self, col_name, figure_name, x_label="time", y_label="",
                              line_color='b', data_range=(0, 24), isNormalized=True):
        """
        默认：调取数据库特定列的前24个数据，归一化处理，绘制蓝色折线图，命名后保存在`/pictures/Figures/`目录下

        参数：
        - col_name : 调取数据库的哪一列
        - figure_name : 图表标题，也是保存的图片名（后缀为.jpg）
        - x_label : x轴标题，默认为 "time"
        - y_label : y轴标题，默认为 col_name
        可更改的默认参数
        - line_color : 默认为'b'（蓝色）
        - data_range : 默认为(0,24)
        - isNormalized : 默认True（归一化）
        """
        # 内部参数设置
        save_path = f"pictures/Figures/{figure_name}.jpg"
        figsize = (9.0, 7.0)
        if y_label == "":
            y_label = col_name

        # 获取数据
        df = self.__fetch_and_prepare_data(col_name, data_range, isNormalized)
        # 绘制并保存图像
        self.__create_plot(df, x_label, y_label, figure_name, save_path, figsize,
                           self.__draw_line_chart, color=line_color)

    # 绘制柱状图 1
    def __draw_bar_graph(self, ax, x_series, y_series, color="g", label=""):
        """绘制包括标签的柱状图"""
        ax.bar(x_series, y_series, color=color, label=label)

    def generate_bar_graph_1(self, col_name, figure_name, x_label="time", y_label="",
                             bar_color='g', data_range=(0, 24), isNormalized=False):
        """
        调取数据库特定列的前24个数据，绘制绿色柱状图，命名后保存在`/pictures/Figures/`目录下

        参数：
        - col_name : 调取数据库的哪一列
        - figure_name : 图表标题，也是保存的图片名（后缀为.jpg）
        - x_label : x轴标题，默认为 "time"
        - y_label : y轴标题，默认为 col_name
        可更改的默认参数
        - bar_color : 默认为'g'（绿色）
        - data_range : 默认为(0,24)
        - isNormalized : 默认False（不归一化）
        """
        # 内部参数设置
        save_path = f"pictures/Figures/{figure_name}.jpg"
        figsize = (9.0, 7.0)
        if y_label == "":
            y_label = col_name

        # 获取数据
        df = self.__fetch_and_prepare_data(col_name, data_range, isNormalized)
        # 绘图并保存
        self.__create_plot(df, x_label, y_label, figure_name, save_path, figsize,
                           self.__draw_bar_graph, color=bar_color, label=y_label)

    def __draw_line_chart_with_point(self, ax, x_series, y_series, line_color="b",
                                     x=0.0, y=0.0, point_color='r', point_marker='o'):
        ax.plot(x_series, y_series, color=line_color)
        ax.plot(x, y, color=point_color, marker=point_marker)

    def generate_line_chart_2(self, col_name, figure_name, x_label="time", y_label="",
                              line_color='b', point_color='r', isNormalized=False):
        """
        根据时间调取数据库特定列的24个数据，绘制蓝色折线图，标注一个红色数据点，命名后保存在`/pictures/Figures/`目录下

        参数：
        - col_name : 调取数据库的哪一列
        - figure_name : 图表标题，也是保存的图片名（后缀为.jpg）
        - x_label : x轴标题，默认为 "time"
        - y_label : y轴标题，默认为 col_name
        可更改的默认参数
        - line_color : 默认为'b'（蓝色）
        - point_color : 默认为 'r' （红色）
        - isNormalized : 默认False（不归一化）
        """
        # 内部参数设置
        save_path = f"pictures/Figures/{figure_name}.jpg"
        figsize = (9.0, 7.0)
        if y_label == "":
            y_label = col_name

        # 时间参数设置
        timer = int(time.time()) % 48  # 每秒+1，30s一轮的时间参数

        # 获取数据
        data_range = (timer, timer + 24)  # 随时间变化的数据范围
        df = self.__fetch_and_prepare_data(col_name, data_range, isNormalized)
        # 绘图并保存
        (x, y) = (timer % 24, df.iloc[timer % 24])
        self.__create_plot(df, x_label, y_label, figure_name, save_path, figsize,
                           self.__draw_line_chart_with_point, line_color=line_color,
                           x=x, y=y, point_color=point_color, point_marker='o')

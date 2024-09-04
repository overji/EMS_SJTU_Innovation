from .ChildPageBase import ChildPage
from APIs.FigureDraw import FigureDraw


class Storage_Ui(ChildPage):

    def __init__(self, relative_path=""):
        super().__init__(relative_path, "storage.ui")

    def timerEvent(self):
        self.update_bar_pic()  # 我也不知道为什么这里是bar而不是line

    def initButton(self):
        # 设置按钮样式
        self.ui.pushButton.setStyleSheet("border-image:url(./pictures/white.png);color: rgb(255, 255, 255);")
        # 连接按钮功能
        self.ui.pushButton.clicked.connect(self.btnClick())  # 加括号是因为这里是一个闭包

    def update_line_pic(self):
        # 生成一张折线图
        FigureDraw().generate_line_chart_1("x_values", "Storage_picture_1", y_label="Total cost ratio")
        # 获取图片并填充控件
        backImagePath = "pictures/Figures/Storage_picture_1.jpg"
        self.ui.PHOTO.setStyleSheet("#PHOTO {border-image: url(" + backImagePath + ");}")
        self.update_label_data()  # 明明什么都没有更新还要调用一次的屑

    def update_bar_pic(self):
        # 生成一张条形图
        FigureDraw().generate_bar_graph_1("BatteryChange", "Storage_picture_2", y_label="Energy(kW)")
        # 获取图片并填充控件
        backImagePath = "pictures/Figures/Storage_picture_2.jpg"
        self.ui.PHOTO.setStyleSheet("#PHOTO {border-image: url(" + backImagePath + ");}")

    def update_label_data(self):
        """更新页面数据的函数。。。但是怎么tm这么抽象；；；明明什么都没干啊为什么就是一个新的函数呢"""
        # # 连接数据库并读取数据（但是为什么没用到）
        # conn = sqlite3.connect("data/data_db.db")
        # query = "SELECT * FROM dataTable"
        # df = pd.read_sql_query(query, conn)

        # 这是什么
        data_column = [0, 500.90, 2.30, 00.00, 100.00, 100.00, 30, 530.65, 229.65, 0.65, 3.00, 1.00, 30, 2.34, 2.26,
                       26.5, 24.00, 99, 97]

        for i in range(1, 19):
            data_label = getattr(self.ui, f"data{i}")  # self.ui.data114
            data_label.setText(f"{data_column[i]:.2f}")

    def btnClick(self):
        """用了一个闭包的写法，记录按钮状态"""
        btnState = 1

        def on_clicked():
            nonlocal btnState
            if btnState == 1:
                self.update_bar_pic()
                btnState = 0
            else:
                self.update_line_pic()
                btnState = 1

        return on_clicked


if __name__ == "__main__":
    from ..APIs.FigureDraw import FigureDraw  # 这句是为了能让本文件检测到这个api然后正确显示代码补全

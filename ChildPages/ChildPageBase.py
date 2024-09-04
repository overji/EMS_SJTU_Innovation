"""
所有子页面的基类
"""
from PyQt5 import uic
import ctypes


class ChildPage:
    """# 包含属性：
    self.ui
    self.relative_path
    # 包含方法（可重写）：
    self.initUi()
    self.setStylesheet()
    self.initButton()
    self.timerEvent()
    """
    ui = None  # 页面ui文件
    relative_path = ""  # 相对于主程序的相对路径

    def __init__(self, relative_path, file_name):
        self.relative_path = relative_path
        self.ui = uic.loadUi(relative_path + file_name)
        self.initUi()
        self.setStylesheet()
        self.initButton()

    def initUi(self):
        pass

    def setStylesheet(self):
        """用于设定统一的样式表，或被重写后设置特定样式表"""
        # 计算字体大小
        standard_font_size = 15
        standard_dpi = 96 * 1.75
        current_dpi = ctypes.windll.user32.GetDpiForWindow(ctypes.windll.user32.GetDesktopWindow())
        font_size = standard_font_size * (current_dpi / standard_dpi)
        # 设置样式表
        stylesheet = f"""
                    font-family:Microsoft YaHei;
                    font-size:{font_size}pt;
                    padding:10px;
                """
        self.ui.setStyleSheet(stylesheet)

    def initButton(self):
        """需重写：按钮初始化，包括图片加载，大小设置，槽函数连接等等"""
        pass

    def timerEvent(self):
        """需重写：定时触发的任务（全局定时器）"""
        pass

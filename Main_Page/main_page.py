from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
import ctypes
class main_page_Ui(QWidget):
    path = None
    def __init__(self, relative_path="",Map=(1000,1000)):
        super().__init__()
        self.Map = Map
        self.path = relative_path
        self.ui = uic.loadUi(self.path + "MainPage.ui")
        #self.ui.setLayout(self.ui.layout)
        text = "\"border-image:url(./pictures/white.png)\""
        for i in range(1,6):
            eval("self.ui.Btn_"+str(i)+".setStyleSheet("+text+")")

        self.ui.Btn_1.clicked.connect(self.Btn_1_click)

        self.myinit()
    def Btn_1_click(self):
        self.ui.label_5.setText("114514")
        print(114514)

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
        self.setStyleSheet(stylesheet)

    def myinit(self):
        self.QHB=QHBoxLayout()
        self.PHOTO = QWidget()
        self.PHOTO.setFixedSize(self.Map[0]//3*2,self.Map[1])
        self.pal = QPalette()
        pal_image = self.myIamge("pictures/backimage/image1.jpg", self.Map[0]//3*2, self.Map[1])  # rr[0] - rr[3], rr[1]
        self.pal.setBrush(self.PHOTO.backgroundRole(), QBrush(pal_image))
        self.PHOTO.setPalette(self.pal)
        self.PHOTO.setAutoFillBackground(True)  # 加上这句，要不不知道为啥图片不显示
        self.PHOTO.setLayout(self.ui.MainPageLayout)


        self.LIST = QWidget()
        self.LIST.setFixedSize(int(self.Map[0]/3.1),self.Map[1])
        self.LIST.setLayout(self.ui.MainDetailLayout)
        self.QHB.addWidget(self.PHOTO)
        self.QHB.addWidget(self.LIST)
        self.setLayout(self.QHB)


    def myIamge(self,text, x, y):
        image1 = QImage(text)
        map = (x, y)
        # map = mymap_long(image1.width(), image1.height(), x, y)
        image2 = image1.scaled(map[0], map[1] - 100)
        # l1 = [(map[0]-x)/2,map[0]-(map[0]-x)/2,(map[1]-y)/2,map[1]-(map[1]-y)/2]
        # image2 = image2.copy(int(l1[0]),int(l1[2]),x,y)
        return image2





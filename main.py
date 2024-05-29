from mainui import *
from SignUp.mainlog import *
from data_input import *

if __name__ == '__main__':
    # 这里更新了数据库里面的数据
    update_data()

    app = QApplication(sys.argv)

    main, wangjimima, register = log_init("SignUp/")
    main.pushButton.clicked.connect(main.cutt)
    main.pushButton_2.clicked.connect(wangjimima.Open3)
    main.pushButton_3.clicked.connect(register.Open2)
    main.pushButton_4.clicked.connect(main.change2)

    main.pushButton_6.clicked.connect(main.change1)

    wangjimima.pushButton_2.clicked.connect(main.Open)
    wangjimima.pushButton.clicked.connect(wangjimima.ct)

    register.pushButton.clicked.connect(register.cut)
    register.pushButton_2.clicked.connect(main.Open)

    main.show()
    main.pushButton_4.close()

    rect = QDesktopWidget().availableGeometry().getRect()
    print(rect)
    rr[0] = rect[2]
    rr[1] = rect[3]
    rr[2] = int(rr[0] / 10)
    rr[3] = rr[2] + 30
    main.setFixedSize(int(rr[0] / 2), int(rr[1] / 2))
    # 创建自定义窗口
    w = MyWindow()
    main.getappfunc(w.show)

    sys.exit(app.exec_())

from mainui import *
from SignUp.mainlog import *


# 登录判定，及成功登录触发事件
def signIn(isDeveloperMode):
    """登录判定，及成功登录触发事件"""
    if isDeveloperMode or mainlogUi.signInTest():  # 若调用时传入1，则跳过登录界面，直接进入主界面
        # 切换到主界面
        mainlogUi.mainUi.close()
        mainWindow.ui.show()

        # 多线程任务
        # thread = threading.Thread(target=runGA)
        # thread.daemon = True
        # thread.start()


# 用于组织页面顶层逻辑
if __name__ == '__main__':
    # 开始程序
    app = QApplication(sys.argv)

    # 登录界面
    mainlogUi = MainLogUi("SignUp/")

    # 程序主界面
    mainWindow = MainWindow()

    # 登录按钮连接到登录判定
    mainlogUi.mainUi.pushButton.clicked.connect(lambda: signIn(0))

    # 打开登录界面
    mainlogUi.mainUi.show()

    # ###################### 跳过登录，直接在主界面调试时使用 ####################################
    signIn(isDeveloperMode=1)
    # ######################################################################################

    # 程序运行
    appexec = app.exec_()
    sys.exit(appexec)

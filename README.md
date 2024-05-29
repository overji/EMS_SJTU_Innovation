# 一、项目架构
## 1. 文件夹概述
在主文件夹下有文件：
- `main.py`：主程序入口
- `mainui.py`：主界面
- `data_input.py`：表格数据转数据库.db
- `mainmenu.ui`：主菜单界面

及文件夹：
- data：
  - `data_db.db`：数据库文件
  - `测试数据.csv`：测试数据
- pictures：存放图片
  - backimage:背景图片
  - button_image：按钮图片
- EV_System
- Wind_System
- Storage_System
- Load_System
- Solar_System
  - `solar.py`
  - `solar.ui`
  - pictures: 存放图片
  - *此外还有一个`__init__.py`文件，用于标识该目录是一个包*

## 2. 界面概述
- 打开`main.py`，进入登录界面`mainlog.py`
- 登陆成功或直接打开`mainui.py`，进入主界面
- 主界面中依次有：
  - 主界面图：未设置
  - 网络界面：未设置
  - 风电系统
  - 光伏系统
  - 电动汽车
  - 储能系统
  - 负荷系统
- 此外，左上角C为单次刷新，T/P为持续刷新和暂停刷新，右上角×为退出

## 3. 命名和编程规范
- 命名规范
  1. 文件夹命名：统一命名为`Xxxx_System`，如`Wind_System`, `Solar_System`。
  2. 文件命名：统一命名为`xxxx.py`，如`wind.py`, `solar.py`。
  3. 文件内类的命名：统一命名为`Xxxx_Ui`，如`Wind_Ui`, `Solar_Ui`。
  4. 其余命名随意，主文件大概率用不到。
<br>

- 编程规范
  1. 路径引用：统一使用以Project为根目录的相对路径。如引用数据库时使用路径`data/data_db.db`。
  2. 类的__init__()方法中，统一传入一个参数`relative_path=None`用于设定类的成员变量`path`，并在类的其他方法中使用`self.path + "路径/路径"`来引用自身所在路径。（自己测试的时候）
<br>

- 字体大小规范：未指定（这也是问题所在喵）

# 二、项目日志
### 2024.3.29，版本0.7.6
1. 项目文件架构整理（除登录界面外已完成）
2. 统一规范未完成
### 2024.5.29，版本0.8.2
1. 更新了风能和光伏发电的ui，取消了电价的图表 
### 2024.5.29，版本0.8.3
1. 将登录界面整合入主程序，以后运行main.py即可运行程序

import pandas as pd
import sqlite3

# 请不要再执行这段代码了，database都被覆盖了
# 此文件留下来是为了防止有新的数据需要使用，制作成csv文件，然后运行改程序即可导入数据库
def update_data():
    return
    # 读取 Excel 文件到 DataFrame
    df = pd.read_csv('测试数据.csv')

    # 连接到 SQLite 数据库
    conn = sqlite3.connect('data_db.db')

    # 将 DataFrame 中的数据写入 SQLite 数据库
    table_name = 'dataTable'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # 关闭数据库连接
    conn.close()

    # 输出成功消息
    print("Data has been written to SQLite database.")

    # 测试用
    # conn = sqlite3.connect("data_db.db")
    # query = "SELECT * FROM dataTable"
    # df = pd.read_sql_query(query,conn)
    # conn.close()
    # print(df)

import pandas as pd
from sqlalchemy import create_engine

def update_data():
    return
    # 读取 CSV 文件到 DataFrame
    df = pd.read_csv('test.csv')

    # 连接到 MySQL 数据库
    engine = create_engine('mysql+mysqlconnector://EMS:282432@112.124.43.86/ems')

    # 将 DataFrame 中的数据写入 MySQL 数据库
    table_name = 'EMS_Data'
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    # 输出成功消息
    print("Data has been written to MySQL database.")

def test():
    engine = create_engine('mysql+mysqlconnector://EMS:282432@112.124.43.86/ems')

    query = "SELECT * FROM EMS_Data"
    df = pd.read_sql(query,engine)

    print(df)

test()
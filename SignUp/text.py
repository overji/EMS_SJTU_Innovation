# !/user/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('user_data.db')
c = conn.cursor()
print('数据库连接成功')
###查询所有数据
sql1 = '''SELECT name,password,number from users'''
c.execute(sql1)

for i in c.execute(sql1):
    print(i)

print('查询成功')

###查询指定数据
xxx = '2'
sql2 = '''SELECT name,password,number from users where (name=:name)'''
c.execute(sql2,{'name': xxx})
for i in c:
    print(i)
print('查询成功')

###查询指定数据的指定部分
xxx = '2'
sql3 = '''SELECT name,password,number from users where (name=:name)'''
c.execute(sql3,{'name': xxx})
print(c.fetchone()[0])
###第几个数据就写几-1，只能用一次
print('查询成功')

###删除指定数据
#xxx = '2'
#sql4 = '''delete from users where (name=:name)'''
#c.execute(sql4,{'name': xxx})
#print('删除成功')

###删除所有数据
#sql5 = '''delete from users'''
#c.execute(sql5)
#print('删除成功')

###修改指定数据
#x = '1233'
#y = 2
#sql6 = '''update users set password=? where name=?'''
#coon = (x, y)
#c.execute(sql6,coon)
#print('修改成功')

conn.commit()
conn.close()

# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 22:47
# @Author  : Li Shuai
# @FileName: demo_pymysql.py
# @Software: PyCharm

import pymysql
import random

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='159357',
                     db='wenda',
                     charset='utf8')

try:
    # 使用 cursor() 方法创建一个游标对象 cursor
    SQL = '''INSERT INTO question(title, content, user_id, created_date, comment_count) values ("姚明", "xxxxxxxx", 5, now(), 0)'''
    with db.cursor() as cursor:
        cursor.execute(SQL)    # 使用 execute()  方法执行 SQL
    db.commit()

    with db.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM question"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

finally:
    db.close()


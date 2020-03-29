# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 18:04:49 2020

@author: Vigneswaran
"""

import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY, USERNAME TEXT, PASSWORD TEXT)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS ITEMS (NAME TEXT, PRICE REAL)"
cursor.execute(create_table)


# user = (1, 'jose', 'asdf')
#
# insert_query = "INSERT INTO USERS VALUES (?, ?, ?)"
# cursor.execute(insert_query, user)
#
# users = [(2, 'rose', 'qwer'), (3, 'bose', 'zxcv'), (4, 'dose', 'asdf')]
# cursor.executemany(insert_query, users)
#
# select_query = "SELECT * FROM USERS"
# for row in cursor.execute(select_query):
#     print(row)
connection.commit()
connection.close()

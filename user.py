# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:47:20 2020

@author: Vigneswaran
"""

import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.username = username
        self.id = _id
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        x = ("****")
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        select_query = "SELECT * FROM USERS WHERE USERNAME=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()
        print(row)
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        select_query = "SELECT * FROM USERS WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        print(row)
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be empty!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be empty!")
    def post(self):
        data = UserRegister.parser.parse_args()

        user = User.find_by_username(data['username'])
        if user:
            return {"message": "User already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO USERS VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {"message": "User created Successfully"}, 201
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 23:19:55 2020

@author: Vigneswaran
"""

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'drrrrk'
api = Api(app)

jwt = JWT(app, authenticate, identity)
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True, use_reloader=False)
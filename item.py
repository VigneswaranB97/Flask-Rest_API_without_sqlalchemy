from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be empty!")

    @jwt_required()
    def get(self, name):
        row = Item.find_by_name(name)
        if row:
            return row
        return {"message": "Item not found"}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM ITEMS WHERE NAME=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"items": {'name': row[0], 'price': row[1]}}, 200

    @classmethod
    def update_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE ITEMS SET PRICE=? WHERE NAME=?"


        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()

    @classmethod
    def insert_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO ITEMS VALUES (?, ?)"

        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM ITEMS WHERE NAME=?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with {} name already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        Item.insert_item(item['name'], item['price'])
        return item, 201

    def delete(self, name):
        if Item.find_by_name(name):
            Item.delete_item(name)
            return {"message": "items deleted"}, 200
        return {"message": "item not found"}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        if Item.find_by_name(name):
            try:
                Item.update_item(name, item['price'])
                return {'message': 'item updated'}
            except:
                return {"message": "An error occured while updating an item"}, 500
        try:
            Item.insert_item(item['name'], item['price'])
            return item, 201
        except:
            return {"message": "An error occured while inserting an item"}, 500


class ItemList(Resource):
    @classmethod
    def get_all_items(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM ITEMS"
        items = []
        for row in cursor.execute(query):
            item = {'name': row[0], 'price': row[1]}
            items.append(item)
        connection.commit()
        connection.close()
        return items

    def get(self):
        items = ItemList.get_all_items()
        return {'items': items}
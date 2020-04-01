from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt

from db_connection import connect
from utilities import get_categories, get_latest_items

def cart_items():
    

def cart_data():
    latest_items = get_latest_items()
    categories = get_categories()

    return items, latest_items, categories, subtotal, items_len

def delete_item(item_id):
    query = "DELETE FROM cart_items WHERE item_id = %s"
    try:
        connection = connect()
        cur = connection.cursor() 
        params = (item_id,)
        cur.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()

def update_item(item_id, quantity, produce_id):
    query = "SELECT produce_quantity FROM produce WHERE produce_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_ii)
        cur.execute(query, params)
        produce_quantity = cur.fetchone()
        if not produce_quantity:
            print("wrong id")
        else:
            if int(quantity) > int(produce_quantity[0]):
                return "Could not update quantity. Total %s kg available" % produce_quantity[0] 
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()

    query = "UPDATE cart_items SET item_quantity = %s WHERE item_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (int(quantity), item_id,)
        cur.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()
    return "Quantity updated successfully"

def add_item(produce_id, quantity):
    buyer_id = session['id']
    query = "INSERT into cart_items (item_id, item_quantity, buyer_id, produce_id) VALUES (UUID(), %s, %s, %s)"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (quantity, buyer_id, produce_id)
        cur.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()
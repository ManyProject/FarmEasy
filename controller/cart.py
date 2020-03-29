from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt
from db_connection import connect

def cart_data():
    query = "SELECT item_id, item_price, item_quantity, item_name,\
         produce_image, produce.produce_id, user_name FROM produce\
         INNER JOIN cart_items ON produce.produce_id = cart_items.produce_id\
         INNER JOIN user ON produce.farmer_id = user.user_id \
         WHERE buyer_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'],)
        cur.execute(query, params)
        items = cur.fetchall()
        if(not items):
            items = []
    except Exception as err:
        return "Error occurred"

    subtotal = 0
    for item in items:
        subtotal += item[1]*item[2]
    items_len = len(items)

    query = "SELECT produce_name, produce_price, produce_image, produce_id, user_name\
         FROM produce INNER JOIN user ON farmer_id = user_id\
         ORDER BY produce_date DESC LIMIT 4"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query)
        latestitems = cur.fetchall()
        if(not latestitems):
            latestitems = []
    except:
        return "Error occurred"
        
    query = "SELECT DISTINCT produce_category FROM produce"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query)
        categories = cur.fetchall()
    except:
        return "SQL Error"
    finally:
        cur.close()
        connection.close()
    return render_template('cart.html', items=items, latestitems=latestitems, categories=categories, subtotal=subtotal, number=items_len)
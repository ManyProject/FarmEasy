from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt
from db_connection import connect

def addproduct(quantity, produce_id):
    produce_quantity = int(quantity)
    query = "SELECT produce_price, produce_quantity, produce_name FROM produce WHERE produce_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_id,)
        cur.execute(query, params)
        produce_detail = cur.fetchone()
        produce_price = produce_detail[0]
        produce_name = produce_detail[2]
    except:
        return "SQL Error"

    buyer_id = session['id']
    query = "INSERT into cart_items (item_id, item_price, item_quantity, item_name, buyer_id, produce_id) VALUES (UUID(), %s, %s, %s, %s, %s)"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_price, produce_quantity, produce_name, buyer_id, produce_id)
        cur.execute(query, params)
    except:
        return "SQL Error"
    return url_for(product , produce_id = produce_id)

def productdetail(produce_id):
    query = "SELECT produce_name, produce_price, user_name, produce_id, produce_quantity, user_address, user_phone, produce_category, produce_image FROM produce INNER JOIN user ON farmer_id = user_id where produce_id = %s" 
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_id,)
        cur.execute(query, params)
        data = cur.fetchone()
        if(not data):
            return "Doesn't exist"
    except:
        return "SQL Error"
        
    produce_category = data[7]
    query = "SELECT produce_name, produce_price, produce_image,produce_id , user_name \
        FROM produce INNER JOIN user ON farmer_id = user_id WHERE produce_category = %s AND produce_id != %s LIMIT 6"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_category,produce_id,)
        cur.execute(query, params)
        relateditems = cur.fetchall()
        if(not relateditems):
            relateditems = []
    except:
        return "SQL Error"
        
    query = "SELECT produce_name, produce_price, produce_image, produce_id, user_name \
        FROM produce INNER JOIN user ON farmer_id = user_id WHERE produce_id != %s ORDER BY produce_date DESC LIMIT 4"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_id,)
        cur.execute(query, params)
        latestitems = cur.fetchall()
        if(not latestitems):
            latestitems = []
    except:
        return "SQL Error"

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
    return render_template('product.html', data = data, relateditems = relateditems, latestitems = latestitems, categories = categories)
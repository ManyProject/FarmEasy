from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt
from db_connection import connect
from utilities import get_categories, get_related_items

def product_detail(produce_id):

    query = "SELECT produce_name, produce_price, user_name, produce_id, produce_quantity, user_address, user_phone,\
         produce_category, produce_image FROM produce INNER JOIN user ON farmer_id = user_id where produce_id = %s" 
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
    finally:
        cur.close()
        connection.close()
        
    produce_category = data[7]
    related_items = get_related_items(produce_category)
    latest_items = get_latest_items()
    categories = get_categories()

    return data, relateditems, latestitems, categories

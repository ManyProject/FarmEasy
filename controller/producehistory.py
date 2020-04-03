from flask import render_template, request, session, flash, redirect, url_for
import mysql.connector
from flask_bcrypt import Bcrypt

from controller.cart import cart_items
from utilities import get_categories
from db_connection import connect

def get_produce():
    query = "SELECT produce_image, produce_name, produce_quantity, produce_date, produce_price, produce_category\
            FROM produce \
            WHERE produce.farmer_id = %s ORDER BY produce_date"
    params = (session['id'],)
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query, params)
        produce_details = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        produce_details = []
        flash("Could not retrieve past Produce details")
    finally:
        cur.close()
        connection.close()
    items, subtotal, items_len = cart_items()
    categories = get_categories() 
    return render_template('producehistory.html', subtotal=subtotal, items=items, produce_details=produce_details, categories=categories)

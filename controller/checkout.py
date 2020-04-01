from flask import render_template, request, session, redirect, url_for
import mysql.connector
from flask_bcrypt import Bcrypt

from db_connection import connect
from utilities import get_categories, get_related_items, get_latest_items

def checkout_page():
    categories = get_categories()
    query = "SELECT buyer_address FROM address WHERE buyer_id = %s"
    try:
        connection = connect()
        cur = connection.cursor() 
        params = (session['id'],)
        cur.execute(query, params)
        buyer_address = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
    return render_template('checkout.html', categories=categories, buyer_address=buyer_address)

def checkout_func():
    # return render_template('delivery_status.html')
    return redirect(url_for('index'))
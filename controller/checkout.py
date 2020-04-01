from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt

from db_connection import connect
from utilities import get_categories, get_related_items, get_latest_items

def checkout_page():
    categories = get_categories()
    query = "SELECT user_address FROM address WHERE user_id=%s"
    try:
        connection = connect()
        cur = connection.cursor() 
        params = (session['id'],)
        cur.execute(query, params)
        connection.commit()
        user_address = cur.fetchall()
    except:
        print("SQL Error")
    finally:
        cur.close()
        connection.close()
    return render_template('checkout.html', categories=categories,user_address=user_address)

def checkout_func():
    # return render_template('delivery_status.html')
    return redirect(url_for('index'))
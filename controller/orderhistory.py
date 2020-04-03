from flask import render_template, request, session, flash
import mysql.connector
from flask_bcrypt import Bcrypt
from db_connection import connect

def order_history():
    query = "SELECT produce_image, produce_name, order_date, user_name, delivery_status,\
            order_quantity, order_price , delivery_address FROM produce \
            INNER JOIN orders ON produce.produce_id = orders.produce_id \
            INNER JOIN user ON produce.farmer_id = user.user_id \
            WHERE orders.buyer_id = %s "
    params = (session['id'],)
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query, params)
        purchased_items = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not retrieve past purchases")
        return []
    finally:
        cur.close()
        connection.close()
    return purchased_items
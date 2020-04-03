from flask import render_template, request, session, flash, redirect, url_for
import mysql.connector
from flask_bcrypt import Bcrypt

from controller.cart import cart_items
from db_connection import connect

def get_status():
    query = "SELECT produce_image, produce_name, order_date, delivery_status,\
            order_quantity, order_price, delivery_address, order_id FROM orders \
            INNER JOIN produce ON orders.produce_id = produce.produce_id \
            WHERE orders.delivery_agency_id = (SELECT agency_id FROM delivery_agent WHERE delivery_agent_id = %s)\
            ORDER BY order_date"
    params = (session['id'],)
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query, params)
        delivery_details = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        delivery_details = []
        flash("Could not retrieve past delivery details")
    finally:
        cur.close()
        connection.close()
    addresses = [delivery[6] for delivery in delivery_details]
    addresses = set(addresses)
    items, subtotal, items_len = cart_items()
    return render_template('delivery.html', subtotal=subtotal, items=items, delivery_details=delivery_details, addresses=addresses)

def set_status(order_id, delivery_status):
    items, subtotal, items_len = cart_items()
    if (not order_id):
        flash("Could not retrieve order")
        return redirect(url_for('delivery'))
    if delivery_status == 'Pending':
        query = "UPDATE orders SET delivery_status = 'Shipping', pickup_time = NOW() WHERE order_id = %s "
    elif delivery_status == 'Shipping':
        query = "UPDATE orders SET delivery_status = 'Delivered', drop_time = NOW() WHERE order_id = %s "
    try:
        connection = connect()
        cur = connection.cursor()
        params = (order_id,)
        cur.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not update status. Try again later")
    finally:
        cur.close()
        connection.close()
    return redirect(url_for('delivery'))
from flask import render_template, request, session, redirect, url_for, flash
import mysql.connector
from flask_bcrypt import Bcrypt

from db_connection import connect
from utilities import get_categories, get_related_items, get_latest_items
from controller.cart import cart_items, delete_item


def checkout_page():
    categories = get_categories()
    items, subtotal, items_len = cart_items()
    query = "SELECT DISTINCT buyer_address FROM address WHERE buyer_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'],)
        cur.execute(query, params)
        buyer_address = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()
    query = "SELECT user_address FROM user WHERE user_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'],)
        cur.execute(query, params)
        user_address = cur.fetchone()
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()
    return render_template('checkout.html', categories=categories,
                           buyer_address=buyer_address, items=items,
                           subtotal=subtotal, items_len=items_len,
                           user_address=user_address)


def checkout_func():
    try:
        connection = connect()
        cur = connection.cursor()
        if(request.form.get('payment_address') == 'existing_address'):
            address = request.form.get('address')
        elif(request.form.get('payment_address') == 'new_address'):
            address = (request.form.get('address', None) + ", "
                    + request.form.get('city', None) + ", "
                    + request.form.get('postcode', None) + ", "
                    + request.form.get('state', None))

            query = "INSERT into address (buyer_id, address_id, buyer_address)\
                    VALUES (%s, UUID(), %s)"
            params = (session['id'], address,)
            cur.execute(query, params)

        items, subtotal, item_len = cart_items()

        orders = []
        for item in items:
            orders.append((item[2], round(item[1]*item[2]*1.2, 2), item[8],
                           'Pending', request.form.get('payment_method', None),
                           address, item[5],))

        values = []
        for order in orders:
            params = (session['id'], order[0], order[1], order[2], order[3],
                      order[4], order[5], order[6],)
            values.append(params)
        query = "INSERT into orders(buyer_id, order_id, order_quantity,\
                 order_date, order_price, delivery_agency_id,\
                 delivery_status, payment_method, delivery_address,\
                 produce_id)\
                 VALUES (%s, UUID(), %s, NOW() , %s, %s, %s, %s, %s, %s)"
        cur.executemany(query, values)

        values = []
        for item in items:
            params = (item[2], item[5],)
            values.append(params)
        query = "UPDATE produce SET produce_quantity = produce_quantity - %s\
                 WHERE produce_id = %s"
        cur.executemany(query, values)

        values = []
        for item in items:
            params = (item[0],)
            values.append(params)

        query = "DELETE FROM cart_items WHERE item_id = %s"
        cur.executemany(query, values)

        connection.commit()
        flash("Order added successfully")
    except mysql.connector.Error as err:
        print(err)
        flash("Could not place your order. Try again later.")
        connection.rollback()
        return redirect(url_for('checkout'))
    finally:
        cur.close()
        connection.close()
    return redirect(url_for('index'))

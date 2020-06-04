from flask import render_template, request, session, flash
import mysql.connector
from flask_bcrypt import Bcrypt

from db_connection import connect
from utilities import get_categories, get_related_items, get_latest_items
from controller.cart import cart_items


def product_detail(produce_id):

    query = "SELECT produce_name, produce_price, user_name, produce_id,\
             produce_quantity, user_address, user_phone,\
             produce_category, produce_image, produce_description FROM produce INNER JOIN user\
             ON farmer_id = user_id where produce_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_id,)
        cur.execute(query, params)
        data = cur.fetchone()
        if(not data):
            print("No data")
            return [], [], [], []
    except mysql.connector.Error as err:
        print(err)
        return [], [], [], []
    finally:
        cur.close()
        connection.close()

    produce_category = data[7]
    relateditems = get_related_items(produce_category)
    latestitems = get_latest_items()
    categories = get_categories()

    if(session.get('email', False)):
        items, subtotal, item_len = cart_items()
    else:
        items, subtotal, item_len = [], 0, 0

    return render_template('product.html', data=data,
                           relateditems=relateditems, latestitems=latestitems,
                           categories=categories, subtotal=subtotal,
                           items=items)

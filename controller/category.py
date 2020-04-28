from flask import render_template, request, session, flash
import mysql.connector
from flask_bcrypt import Bcrypt

from db_connection import connect
from utilities import get_categories, get_latest_items
from controller.cart import cart_items


def category_page(category):
    quantity_list = request.args.getlist('quantity')
    price_list = request.args.getlist('price')

    if(len(price_list)):
        s = "0"
    else:
        s = "1"
    for price in price_list:
        if(price == '100'):
            s += " OR produce_price < 100"
        if(price == '500'):
            s += " OR produce_price > 100 AND produce_price <= 500"
        if(price == '1000'):
            s += " OR produce_price > 500 AND produce_price <= 1000"
        if(price == '10000'):
            s += " OR produce_price > 1000"

    if(len(quantity_list)):
        q = "0"
    else:
        q = "1"
    for quantity in quantity_list:
        if(quantity == '100'):
            q += " OR produce_quantity < 100"
        if(quantity == '200'):
            q += " OR produce_quantity > 100 AND produce_quantity <= 200"
        if(quantity == '500'):
            q += " OR produce_quantity > 200 AND produce_quantity <= 500"
        if(quantity == '10000'):
            q += " OR produce_quantity > 500"

    sort = request.args.get("sort", "produce_name ASC")

    page = request.args.get('page', 1)
    categories = get_categories()
    latest = get_latest_items()
    if(session.get('email', False)):
        items, subtotal, items_len = cart_items()
    else:
        items, subtotal, items_len = [], 0, 0

    query = "SELECT produce_image, produce_name, produce_price, produce_id,\
            produce_quantity FROM produce WHERE \
            produce_category = %s AND produce_quantity != 0\
            AND (" + s + ") AND (" + q + ")" + " ORDER BY \
            " + sort

    try:
        connection = connect()
        cur = connection.cursor()
        params = (category,)
        cur.execute(query, params)
        category = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()

    return render_template('category.html', items=items,
                           subtotal=subtotal, categories=categories,
                           latestitems=latest, category=category,
                           total=len(category),
                           page=page)

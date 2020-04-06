from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

from db_connection import connect
from controller.cart import cart_items

def get_produce_page():
    # query = ""
    # try:
    #     connection = connect()
    #     cur = connection.cursor()
    #     params = (,)
    #     cur.execute(query, params)
    #     connection.commit()
    # except mysql.connector.Error as err:
    #     print(err)
    #     flash("Could not update status. Try again later")
    # finally:
    #     cur.close()
    #     connection.close()
    return render_template('pages-ecommerce-product-add.html')

def set_produce():
    return 0
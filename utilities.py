from flask import flash, session
import mysql.connector

from db_connection import connect

def get_categories():
    query = "SELECT DISTINCT produce_category FROM produce"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query)
        categories = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        return []
    finally:
        cur.close()
        connection.close()
    return categories

def get_related_items(produce_category):
    query = "SELECT produce_name, produce_price, produce_image, produce_id , user_name \
        FROM produce INNER JOIN user ON farmer_id = user_id \
        WHERE produce_category = %s AND produce_quantity != 0 LIMIT 7"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (produce_category,)
        cur.execute(query, params)
        related_items = cur.fetchall()
        if(not related_items):
            related_items = []
    except mysql.connector.Error as err:
        print(err)
        return []
    finally:
        cur.close()
        connection.close()
    return related_items

def get_latest_items():
    query = "SELECT produce_name, produce_price, produce_image, produce_id, user_name \
        FROM produce INNER JOIN user ON farmer_id = user_id WHERE produce_quantity <> 0 ORDER BY produce_date DESC LIMIT 5"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query)
        latest_items = cur.fetchall()
        if(not latest_items):
            latest_items = []
    except mysql.connector.Error as err:
        print(err)
        return []
    finally:
        cur.close()
        connection.close()
    return latest_items

def get_perm_address():
    query = "SELECT user_address FROM user WHERE user_id = %s "
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'],)
        cur.execute(query, params)
        perm_addr = cur.fetchone()
        perm_address = perm_addr[0]
    except mysql.connector.Error as err:
        print(err)
        flash("Could not obtain address")
        return "Not Found"
    finally:
        cur.close()
        connection.close()
    return perm_address

def get_buyer_address():
    query = "SELECT buyer_address FROM address WHERE buyer_id = %s "
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'],)
        cur.execute(query, params)
        buyer_address = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not obtain address")
        return []
    finally:
        cur.close()
        connection.close()
    return buyer_address

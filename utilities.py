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
        FROM produce INNER JOIN user ON farmer_id = user_id WHERE produce_category = %s LIMIT 7"
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
        FROM produce INNER JOIN user ON farmer_id = user_id ORDER BY produce_date DESC LIMIT 5"
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
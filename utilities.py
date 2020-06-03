import os

from flask import flash, session
import mysql.connector
import urllib.request
import urllib.parse

from db_connection import connect


def sendSMS(numbers, message):
    print(message)
    # message = urllib.parse.urlencode(message)
    print(message)
    pre = {'apikey': os.environ.get('api'),
           'numbers': '91' + numbers,
           'message': message, 'sender': 'TXTLCL'}
    print(pre)
    data = urllib.parse.urlencode(pre)

    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    print(fr)
    return(fr)


def get_categories():
    query = "SELECT DISTINCT produce_category FROM produce\
             WHERE produce_quantity <> 0 ORDER BY produce_category"
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
    query = "SELECT produce_name, produce_price, produce_image,\
            produce_id , user_name FROM produce INNER JOIN user \
            ON farmer_id = user_id \
            WHERE produce_category = %s AND produce_quantity <> 0 LIMIT 7"
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
    query = "SELECT produce_name, produce_price, produce_image, produce_id,\
            user_name FROM produce INNER JOIN user ON farmer_id = user_id \
            WHERE produce_quantity <> 0 ORDER BY produce_date DESC LIMIT 5"
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


def category_items(category):
    query = "SELECT produce_image, produce_name, produce_price, produce_id\
             FROM produce WHERE produce_category = %s\
             AND produce_quantity != 0 \
             ORDER BY RAND() LIMIT 7"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (category,)
        cur.execute(query, params)
        items = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        return []
    finally:
        cur.close()
        connection.close()
    return items


def get_agencies():
    query = "SELECT agency_id, agency_name, intercity_rates, intracity_rates\
             FROM delivery_agency ORDER BY agency_id"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query)
        delivery_details = cur.fetchall()
        print('success')
        print(delivery_details)
    except mysql.connector.Error as err:
        print(err)
        delivery_details = []
    finally:
        cur.close()
        connection.close()
    return delivery_details


def show_produce(farmer_id):
    query = "SELECT produce_image, produce_name, produce_quantity,\
            produce_date, produce_price, produce_category\
            FROM produce \
            WHERE produce.farmer_id = %s ORDER BY produce_date LIMIT 1"
    params = (farmer_id,)
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query, params)
        produce_details = cur.fetchall()
        print('success')
        print(produce_details)
    except mysql.connector.Error as err:
        print(err)
        produce_details = []
    finally:
        cur.close()
        connection.close()
        print(len(produce_details))
        if(len(produce_details) > 0):
            s = ""
            for produce in produce_details:
                s += "Name: " + str(produce[1])
                s += "\nQuantity: " + str(produce[2])
                s += "\nDate: " + str(produce[3])
                s += "\nPrice: " + str(produce[4])
                s += "\nCategory: " + str(produce[5])
        else:
            s = "No produce found"
        return s


def add_produce_sms(content, farmer_id):
    name = str(content[0])
    price = int(content[1])
    quantity = int(content[2])
    category = str(content[3])
    del_agency = int(content[4])
    delivery_agency = get_agencies()
    query = "INSERT INTO produce(produce_id, farmer_id, produce_name,\
             produce_date, produce_category,\
             produce_quantity, produce_price, delivery_agency_id)\
             VALUES (UUID(), %s, %s, NOW(), %s, %s, %s, %s)"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (farmer_id, name, category, quantity, price,
                  delivery_agency[del_agency-1][0],)
        cur.execute(query, params)
        connection.commit()
        print('succ')
    except mysql.connector.Error as err:
        print(err)
        return False
    finally:
        cur.close()
        connection.close()
    return True


def show_agencies():
    delivery_agencies = get_agencies()
    print(len(delivery_agencies))
    s = ""
    cnt = 0
    for agency in delivery_agencies:
        cnt += 1
        s += str(cnt) + ") Name: " + str(agency[1])
        s += "\nIntracity Rates: " + str(agency[2])
        s += "\nIntercity Rates: " + str(agency[3]) + "\n"
    return s

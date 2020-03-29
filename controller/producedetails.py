from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt

def connect():
    return mysql.connector.connect(host="localhost",database='farmeasy', user="root", passwd="")

def productdetail(pname):
    query = "SELECT produce_name, produce_price, user_name, produce_id, produce_quantity, user_address, user_phone, produce_category, produce_image FROM produce INNER JOIN user ON farmer_id = user_id where produce_name = "+"'"+pname+"'"
    connection = connect()
    cur = connection.cursor()
    cur.execute(query)
    data = cur.fetchone()
    pcategory = data[7]
    pid = data[3]
    query = "SELECT produce_name, produce_price, produce_image FROM produce where produce_category = "+"'"+pcategory+"' AND produce_id != '"+ pid +"' LIMIT 6"
    connection = connect()
    cur = connection.cursor()
    cur.execute(query)
    relateditems = cur.fetchall()
    query = "SELECT produce_name, produce_price, produce_image FROM produce WHERE produce_id != '"+ pid +"'ORDER BY produce_date DESC LIMIT 4"
    connection = connect()
    cur = connection.cursor()
    cur.execute(query)
    latestitems = cur.fetchall()
    query = "SELECT DISTINCT produce_category FROM produce"
    connection = connect()
    cur = connection.cursor()
    cur.execute(query)
    categories = cur.fetchall()
    return render_template('product.html', data = data, relateditems = relateditems, latestitems = latestitems, categories = categories)
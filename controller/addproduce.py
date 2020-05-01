from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
import mysql.connector
from datetime import datetime

from db_connection import connect
from controller.cart import cart_items
from utilities import get_categories


def validate(request):
    form = request.form
    check = all(item in ['produce_name', 'produce_date',
                         'category', 'produce_price', 'produce_quantity',
                         'delivery_agency', 'produce_description',
                         'submit'] for item in form.keys())
    return check and ('produce_img' in request.files)


def get_agencies():
    query = "SELECT agency_id, agency_name, intracity_rates,\
             intercity_rates FROM delivery_agency"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query)
        agencies = cur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not fetch agencies. Try again later")
        return []
    finally:
        cur.close()
        connection.close()
    agencies = [[str(attribute) for attribute in agency]
                for agency in agencies]
    return agencies


def get_produce_page():
    agencies = get_agencies()
    return render_template('addproduct.html', agencies=agencies)


def set_produce():
    form = request.form
    if(not validate(request)):
        flash("Not all input fields were completed. Try again")
        return redirect(url_for('add_produce'))

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    if('produce_img' in request.files):
        image_name = request.files['produce_img'].filename
        image_ext = image_name.split('.', 1)[1].lower()
        if (image_ext not in ALLOWED_EXTENSIONS):
            flash("Allowed Extensions are : jpg, jpeg, png ")
        image_name = (form['produce_name'] + "-" +
                      str(datetime.now().strftime("%d%m%y %H%M%S"))
                      + "." + image_ext)
        image_path = "./static/produce-images/" + image_name
        request.files['produce_img'].save(image_path)

    query = "INSERT INTO produce(produce_id, farmer_id, produce_name,\
             produce_date, produce_image, produce_category,\
             produce_quantity, produce_price, delivery_agency_id,\
             produce_description)\
             VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'], form['produce_name'], form['produce_date'],
                  image_path[1:], form['category'],
                  form['produce_quantity'], form['produce_price'],
                  form['delivery_agency'], form['produce_description'])
        cur.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not add your Product. Try again later")
        return redirect(url_for('add_produce'))
    finally:
        cur.close()
        connection.close()
    flash("Successfully added produce")
    return redirect(url_for('add_produce'))

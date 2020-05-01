from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
import mysql.connector
from datetime import datetime
from flask_bcrypt import Bcrypt

from db_connection import connect
from controller.cart import cart_items
import os


def get_details():
    query = "SELECT user_image, user_name, user_email, user_phone, \
             user_address, user_role FROM user WHERE user_id = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        params = (session['id'],)
        cur.execute(query, params)
        user_details = cur.fetchone()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not get your details. Try again Later")
        return []
    finally:
        cur.close()
        connection.close()
    return user_details


def get_profile():
    user_details = get_details()
    items, subtotal, items_len = cart_items()
    return (render_template('profile.html', user_details=user_details,
            items=items, subtotal=subtotal))


def set_profile():
    form = request.form
    user_details = get_details()

    fname = form['first_name']
    lname = form['last_name']
    user_name = fname + " " + lname
    user_phone = form['phone']
    user_address = form['address']
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    form = request.form
    image_path = user_details[0]
    print("name" + request.files['image'].filename)
    if(request.files['image'].filename == ""):
        query = "UPDATE user SET user_name = %s, user_phone = %s,\
                user_address = %s WHERE user_id = %s"
        params = (user_name, user_phone, user_address,
                    session['id'],)
    
    elif(request.files['image'].filename != ""):
        image_name = request.files['image'].filename
        image_ext = image_name.split('.', 1)[1].lower()
        if (image_ext not in ALLOWED_EXTENSIONS):
            flash("Allowed Extensions are : jpg, jpeg, png ")
        image_name =(user_name + "-" +
                     str(datetime.now().strftime("%d%m%y %H%M%S"))
                     + "." + image_ext)
        print(image_name)
        image_path = "./static/user_profile_image/" + image_name
        print(image_path)
        request.files['image'].save(image_path)

        query = "UPDATE user SET user_image = %s, user_name = %s, user_phone = %s,\
                user_address = %s WHERE user_id = %s"
        params = (image_path[1:], user_name, user_phone, user_address,
                    session['id'],)
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query, params)
        connection.commit()
        flash("Profile updated successfully!!")
    except mysql.connector.Error as err:
        print(err)
        flash("Could not update your details. Try again Later")
    finally:
        cur.close()
        connection.close()
    return redirect(url_for('profile'))


def get_update_page():
    user_details = get_details()
    items, subtotal, items_len = cart_items()
    return render_template('password.html', user_details=user_details,
                           items=items, subtotal=subtotal)


def set_pass(app):
    form = request.form
    pwd = form['password']
    pwd_repeat = form['confirm']

    if (pwd != pwd_repeat):
        flash("Different passwords.")
        return redirect(url_for('updatepassword'))

    query = "UPDATE user SET user_password = %s WHERE user_id = %s"
    try:
        connection = connect()
        bcrypt = Bcrypt(app)
        pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
        cur = connection.cursor()
        params = (pw_hash, session['id'],)
        cur.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(err)
        flash("Could not update your details. Try again Later")
    finally:
        cur.close()
        connection.close()
    return redirect(url_for('updatepassword'))

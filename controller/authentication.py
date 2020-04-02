from flask import render_template, request, session, redirect, url_for
import mysql.connector
from flask_bcrypt import Bcrypt
from functools import wraps
import re 

from db_connection import connect

def authentication_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            if(request.endpoint == 'auth' or request.endpoint == 'registration'):
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        else:
            if(request.endpoint == 'auth' or request.endpoint == 'registration'):
                return f(*args, **kwargs)
            return redirect(url_for('auth'))
    return decorated_function
    
def login(app):
    form = request.form
    bcrypt = Bcrypt(app)
    email = form['email']
    password = form['password']
    query = "SELECT user_password, user_role, user_id, user_email FROM user WHERE user_email = %s"
    try:
        connection = connect()
        cur = connection.cursor()
        cur.execute(query, (email, ))
        results = cur.fetchall()
        if len(results) > 0:
            results = results[0]
            if bcrypt.check_password_hash(results[0], password):
                session['email'] = results[3]
                session['role'] = results[1]
                session['id'] = results[2]
                return redirect(url_for('index'))
            else:
                return redirect(url_for('auth'))
        else:
            return redirect(url_for('auth'))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return "SQL ERROR"
    finally:
        cur.close()
        connection.close()

def register(app):
    form = request.form
    fname = form['firstname']
    lname = form['lastname']
    name = fname + " " + lname
    email = form['email']
    phone = form['phone']
    addr = form['address']
    role = form['role']
    pwd = form['password']
    pwd_repeat = form['confirm']

    ip_vars = [fname, lname, email, phone, addr, role, pwd, pwd_repeat]

    address = ['Mumbai','Delhi','Pune','Banglore','Kolkata']

    if(None in ip_vars):
        return "Incomplete form"
    if(pwd != pwd_repeat):
        return redirect(url_for('registration'))
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(not re.search(regex,email)):  
        return redirect(url_for('registration'))
    try:
        connection = connect()
        bcrypt = Bcrypt(app)
        pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
        cur = connection.cursor()
        query = "INSERT INTO user(user_id, user_name, user_email, user_phone, user_role, user_password)\
             VALUES(UUID(), %s, %s, %s, %s, %s)"
        cur.execute(query, (name, email, phone, addr, role, pw_hash, ))
        connection.commit()
        sql = "INSERT INTO address VALUES (%s, UUID(), %s)"
        x = random.randint(0, len(address)-1)
        params = (uid, address[x],)
        cur.execute(sql, params) 
        cur.commit() 
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
        connection.close()
    return redirect(url_for('index'))
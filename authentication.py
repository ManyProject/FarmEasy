from flask import render_template, request, session
import mysql.connector
from flask_bcrypt import Bcrypt

def connect():
    return mysql.connector.connect(host="localhost",database='farmeasy', user="root", passwd="")

def authenticate(app):
    if request.method == 'GET' :
        return render_template('login.html')
    if request.method == 'POST' :
        form = request.form
        if form['active-log-panel'] == 'register':
            register(app)
            return render_template('login.html')
        else:
            bcrypt = Bcrypt(app)
            email = form['email']
            password = form['password']
            query = "SELECT user_pass, user_role FROM user WHERE user_email = '%s'"
            try:
                connection = connect()
                cur = connection.cursor()
                cur.execute(query, (email, ))
                connection.commit()
                role = cur.fetchall()
                if len(role) > 0:
                    if bcrypt.check_password_hash(role[0][0], password):
                        session['email'] = email
                        session['role'] = role[0][1]
                        return render_template('market.html')
                    else:
                        return render_template('login.html', 'pwd-incorrect')
                else:
                    return render_template('login.html', 'email-incorrect')
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
            cur.close()    

def register(app):
    form = request.form
    name = form['name']
    email = form['email']
    phone = form['phone']
    addr = form['addr']
    role = form['role']
    pwd = form['password']
    try:
        connection = connect()
        bcrypt = Bcrypt(app)
        pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
        cur = connection.cursor()
        query = "INSERT INTO user(user_id, user_name, user_email, user_phone, user_address, user_role, user_pass) VALUES(UUID(), '%s', '%s', '%s', '%s', '%s', '%s')"
        cur.execute(query, (name, email, phone, addr, role, pwd, ))
        connection.commit()
        cur.close()
    except expression as identifier:
        pass
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

from authentication import login, register, authentication_check

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])

def index():
    return "Hello"

@app.route('/login', methods=['GET', 'POST'])

def auth():
    if request.method == 'GET' :
        return render_template('login.html')
    if request.method == 'POST' :
        return login(app)

@app.route('/register', methods=['GET', 'POST'])

def registration():
    if request.method == 'GET' :
        return render_template('register.html')
    if request.method == 'POST' :
        return register(app)

@app.route('/logout', methods=['GET'])

def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
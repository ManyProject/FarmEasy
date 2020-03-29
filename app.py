from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

from controller.authentication import login, register, authentication_check
from controller.producedetails import productdetail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])

def index():
    return render_template('category.html')

@app.route('/category')

def category():
    return render_template('category.html')

@app.route('/product/<pname>')

def product(pname):
    return productdetail(pname)

@app.route('/login', methods=['GET', 'POST'])
@authentication_check
def auth():
    if request.method == 'GET' :
        return render_template('login.html')
    if request.method == 'POST' :
        return login(app)

@app.route('/register', methods=['GET', 'POST'])
@authentication_check
def registration():
    if request.method == 'GET' :
        return render_template('register.html')
    if request.method == 'POST' :
        return register(app)

@app.route('/logout', methods=['GET'])

def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/main', methods=['GET'])
@authentication_check
def main():
    return "logged in"

if __name__ == '__main__':
    app.run(debug=True)
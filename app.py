from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from controller.authentication import login, register, authentication_check
from controller.produce import productdetail, addproduct
from controller.cart import cart_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])

def index():
    return "hello"

@app.route('/cart')
@authentication_check
def cart():
    return cart_data()

@app.route('/product/<produce_id>')
@authentication_check
def product(produce_id):
    if request.method == 'POST':
        quantity = request.form['quantity']
        produce_id = request.form['produce_id']
        return addproduct(quantity, produce_id)
    return productdetail(produce_id)

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
    session.pop('role', None)
    session.pop('id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
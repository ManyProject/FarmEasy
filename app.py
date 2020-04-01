from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

from controller.authentication import login, register, authentication_check
from controller.produce import product_detail
from controller.cart import cart_data, delete_item, update_item, add_item
from controller.checkout import checkout_page, checkout_func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])

def index():
    return "hello"

@app.route('/cart')
@authentication_check
def cart():
    items, latestitems, categories, subtotal, items_len =  cart_data()
    return render_template('cart.html', items=items, latestitems=latestitems, categories=categories, subtotal=subtotal, number=items_len)

@app.route('/cart_item', methods = ['POST'])
@authentication_check
def item():
    if(request.form.get('type', None) == 'delete'):
        delete_item(request.form.get('item_id'))
        return redirect(url_for(request.form.get('endpoint', 'cart'))) 
    elif(request.form.get('type', None) == 'update'):
        msg = update_item(request.form.get('item_id', None), request.form.get('quantity', None), request.form.get('produce_id', None),)
        flash(msg)
        return redirect(url_for(request.form.get('endpoint', 'cart'))) 
    elif(request.form.get('type', None) == 'add'):
        add_item(request.form.get('produce_id', None), request.form.get('quantity', None))
        return redirect(url_for(request.form.get('endpoint', 'cart'))) 

@app.route('/product/<produce_id>', methods = ['GET', 'POST'])
@authentication_check
def product(produce_id):
    items, latestitems, categories, subtotal, items_len = cart_data()
    data, relateditems, latestitems, categories = product_detail(produce_id) 
    return render_template('product.html', data=data, relateditems=relateditems, latestitems=latestitems, categories=categories,
                            subtotal=subtotal, items=items)

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

@app.route('/checkout',methods=['GET', 'POST'])
@authentication_check
def checkout():
    if(request.method == 'GET'):
        return checkout_page()
    else:
        return checkout_func()

if __name__ == '__main__':
    app.run(debug=True)
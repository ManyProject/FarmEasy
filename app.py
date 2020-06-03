from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash)
import mysql.connector
from flask_compress import Compress

from controller.authentication import (login, register, authentication_check,
                                       farmer_check, buyer_check, agent_check)
from controller.produce import product_detail
from controller.cart import (cart_data, delete_item, update_item,
                             add_item, cart_items)
from controller.checkout import checkout_page, checkout_func
from controller.orderhistory import order_history
from controller.delivery import get_status, set_status
from controller.producehistory import get_history
from controller.profile import (get_profile, set_profile,
                                get_update_page, set_pass)
from controller.addproduce import get_produce_page, set_produce
from controller.category import category_page
from utilities import (get_perm_address, get_buyer_address, category_items,
                       get_categories, get_latest_items, sendSMS, get_agencies,
                       show_produce, add_produce_sms, show_agencies)
from db_connection import connect

app = Flask(__name__)
Compress(app)

app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = '/static/user_profile_images'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024


@app.before_request
def before_request():
    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)


@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    categories = get_categories()
    latest = get_latest_items()
    cat_items = [category_items(category[0])
                 for category in categories]
    if(session.get('email', False)):
        if(session['role'] == "Farmer"):
            return redirect(url_for('producehistory'))
        if(session['role'] == "Delivery Agent"):
            return redirect(url_for('delivery'))
        items, subtotal, items_len = cart_items()
        return render_template('index-2.html', items=items,
                               subtotal=subtotal,
                               category_items=cat_items,
                               categories=categories, latest=latest)
    return render_template('index-2.html', categories=categories,
                           category_items=cat_items, latest=latest)


@app.route('/category/<category>')
def category(category):
    return category_page(category)


@app.route('/about-us')
def about():
    if(session.get('email', False)):
        items, subtotal, items_len = cart_items()
    else:
        items, subtotal, items_len = [], 0, 0
    return render_template('about-us.html',  items=items,
                           subtotal=subtotal,
                           items_len=items_len)


@app.route('/contact-us')
def contact():
    if(session.get('email', False)):
        items, subtotal, items_len = cart_items()
    else:
        items, subtotal, items_len = [], 0, 0
    return render_template('contact.html',  items=items,
                           subtotal=subtotal,
                           items_len=items_len)


@app.route('/cart')
@authentication_check
@buyer_check
def cart():
    items, latestitems, categories, subtotal, items_len = cart_data()
    return render_template('cart.html', items=items, latestitems=latestitems,
                           categories=categories, subtotal=subtotal,
                           number=items_len)


@app.route('/cart_item', methods=['POST'])
@authentication_check
@buyer_check
def item():
    if(request.form.get('type', None) == 'delete'):
        delete_item(request.form.get('item_id'))
        return redirect(request.referrer)
    elif(request.form.get('type', None) == 'update'):
        msg = update_item(request.form.get('item_id', None),
                          request.form.get('quantity', None),
                          request.form.get('produce_id', None),)
        flash(msg)
        return redirect(request.referrer)
    elif(request.form.get('type', None) == 'add'):
        add_item(request.form.get('produce_id', None),
                 request.form.get('quantity', None))
        return redirect(request.referrer)


@app.route('/product/<produce_id>', methods=['GET', 'POST'])
def product(produce_id):
    return product_detail(produce_id)


@app.route('/checkout', methods=['GET', 'POST'])
@authentication_check
@buyer_check
def checkout():
    if(request.method == 'GET'):
        return checkout_page()
    if(request.method == 'POST'):
        return checkout_func()


@app.route('/history')
@authentication_check
@buyer_check
def history():
    items, subtotal, items_len = cart_items()
    perm_address = get_perm_address()
    buyer_address = get_buyer_address()
    purchased_items = order_history()
    return render_template('orderhistory.html', items=items, subtotal=subtotal,
                           items_len=items_len,
                           purchased_items=purchased_items,
                           perm_address=perm_address,
                           buyer_address=buyer_address)


@app.route('/delivery', methods=['GET', 'POST'])
@authentication_check
@agent_check
def delivery():
    if request.method == 'GET':
        return get_status()
    if request.method == 'POST':
        return set_status(request.form.get('order_id', None),
                          request.form.get('delivery_status', None))


@app.route('/produce-history')
@authentication_check
@farmer_check
def producehistory():
    return get_history()


@app.route('/profile', methods=['GET', 'POST'])
@authentication_check
def profile():
    if(request.method == 'GET'):
        return get_profile()
    if request.method == 'POST':
        return set_profile()


@app.route('/add-produce', methods=['GET', 'POST'])
@authentication_check
@farmer_check
def add_produce():
    if request.method == 'GET':
        return get_produce_page()
    if request.method == 'POST':
        return set_produce()


@app.route('/update-password', methods=['GET', 'POST'])
@authentication_check
def updatepassword():
    if request.method == 'GET':
        return get_update_page()
    if request.method == 'POST':
        return set_pass(app)


@app.route('/login', methods=['GET', 'POST'])
@authentication_check
def auth():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        return login(app)


@app.route('/register', methods=['GET', 'POST'])
@authentication_check
def registration():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        return register(app)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    session.pop('role', None)
    session.pop('id', None)
    session.pop('url', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.route('/sms', methods=['POST'])
def sms():
    print(request.form)
    body = request.form
    content = body['content']
    sender = body['sender'][2:]

    cnt = content.split('\n')
    print(cnt)

    if(cnt[1].lower() == 'help'):
        s = "1) ADD\n"

        s += "Format your message as given below:\n"

        s += "ADD\n<Name>\n<Price>\n<Quantity>\n<Category>\
            \n<Description>\
            \n<Delivery Agency>\
            \n\n"

        s += "2) SHOW LATEST PRODUCE\n\n"

        s += "3) DELIVERY AGENCIES"
        sendSMS(sender, s)
        print(s)

    if(cnt[1].lower() == 'add'):
        if(len(cnt[2:]) == 6):
            query = "SELECT user_id FROM user WHERE user_phone = %s"
            try:
                connection = connect()
                cur = connection.cursor()
                params = (sender,)
                cur.execute(query, params)
                farmer_id = cur.fetchone()
                farmer_id = farmer_id[0]
                print(farmer_id)
                ret = add_produce_sms(cnt[2:], farmer_id)
                if(ret):
                    sendSMS(sender, "Produce added successfully")
                    print("s")
            except mysql.connector.Error as err:
                print(err)
            finally:
                cur.close()
                connection.close()

    if(cnt[1].lower().replace(" ", "") == 'showlatestproduce'):
        query = "SELECT user_id FROM user WHERE user_phone = %s"
        try:
            connection = connect()
            cur = connection.cursor()
            params = (sender,)
            cur.execute(query, params)
            farmer_id = cur.fetchone()
            farmer_id = farmer_id[0]
            print(farmer_id)
            s = show_produce(farmer_id)
            sendSMS(sender, s)
            print(s)
        except mysql.connector.Error as err:
            print(err)
        finally:
            cur.close()
            connection.close()

    if(cnt[1].lower().replace(" ", "") == 'deliveryagencies'):
        query = "SELECT user_id FROM user WHERE user_phone = %s"
        try:
            connection = connect()
            cur = connection.cursor()
            params = (sender,)
            cur.execute(query, params)
            farmer_id = cur.fetchone()
            farmer_id = farmer_id[0]
            print(farmer_id)
            s = show_agencies()
            sendSMS(sender, s)
            print(s)
        except mysql.connector.Error as err:
            print(err)
        finally:
            cur.close()
            connection.close()
    return "1"


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

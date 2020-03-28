from flask import Flask, render_template, request, redirect
import mysql.connector

from authentication import authenticate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if(request.method == 'POST'):
        return render_template('category.html')

@app.route('/cart/<a>')

def cart(a):
    print(a)
    return render_template('category.html')

if __name__ == '__main__':
    app.run(debug=True)
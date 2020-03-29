from flask import Flask, render_template, request, redirect
import mysql.connector

from authentication import authenticate 
from producedetails import productdetail

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    return render_template('category.html')

@app.route('/category')

def category():
    return render_template('category.html')

@app.route('/product/<pname>')

def product(pname):
    return productdetail(pname)

if __name__ == '__main__':
    app.run(debug=True)
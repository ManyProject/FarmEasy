from flask import Flask, render_template, request, redirect
import mysql.connector

from authentication import authenticate 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    return authenticate(app)

if __name__ == '__main__':
    app.run(debug=True)
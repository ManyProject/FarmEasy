import mysql.connector
import os

def connect():
    return mysql.connector.connect(
        host = os.environ.get('MYSQL_HOST', "localhost"),
        user = os.environ.get('MYSQL_USER', "root"),
        passwd = os.environ.get('MYSQL_PWD', ""),
        database = os.environ.get('MYSQL_DB', "farmeasy"),
        port = os.environ.get('MYSQL_PORT', "3306")
    )



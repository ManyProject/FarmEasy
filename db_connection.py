import mysql.connector

def connect():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "farmeasy",
        port = "3306"
    )
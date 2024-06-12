import mysql.connector
from datetime import datetime

def connect_to_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="Vishal@2515",  # Replace with your MySQL password
        database="cafetaria", auth_plugin='mysql_native_password'
    )
    return conn

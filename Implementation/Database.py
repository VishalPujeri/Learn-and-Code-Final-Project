import mysql.connector

def connect_to_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Vishal@2515",
        database="cafetaria", auth_plugin='mysql_native_password'
    )
    return conn

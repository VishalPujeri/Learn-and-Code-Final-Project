import mysql.connector
from core.Exception import DatabaseConnectionError

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Vishal@2515",
            database="cafetaria",
            auth_plugin='mysql_native_password'
        )
        return conn
    except mysql.connector.Error as err:
        raise DatabaseConnectionError(f"Error connecting to the database: {err}")

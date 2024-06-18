from Database import connect_to_db
from Validation import Validation
from Cafeteria import MenuItem, Feedback, Recommendation, UserPreference
from datetime import datetime

class User:
    def __init__(self, user_id, user_name, user_role):
        self.user_id = user_id
        self.user_name = user_name
        self.user_role = user_role

    @staticmethod
    def login(user_id, user_password):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE user_id = %s AND password = %s", (user_id, user_password))
            user = cursor.fetchone()
            if user:
                return User(user[0], user[1], user[2])
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    @staticmethod
    def register(user_id, user_name, user_role, user_password):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (user_id, user_name, user_role, password) VALUES (%s, %s, %s, %s)", 
                           (user_id, user_name, user_role, user_password))
            conn.commit()
            return User(user_id, user_name, user_role)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

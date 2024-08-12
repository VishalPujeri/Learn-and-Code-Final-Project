from data.Database import connect_to_db
from service.Validation import Validation
from utils.logger import log_activity
from core.Exception import DatabaseConnectionError, InvalidInputError

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
            cursor.execute(
                "SELECT * FROM Users WHERE user_id = %s AND password = %s", 
                (user_id, user_password)
            )
            user = cursor.fetchone()
            if user:
                log_activity(user_id, 'login')
                return User(user[0], user[1], user[2])
            return None
        except Exception as e:
            raise DatabaseConnectionError(f"Database connection error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def register(user_id, user_name, user_role, user_password):
        if not user_id or not user_name or not user_role or not user_password:
            raise InvalidInputError("All user details must be provided for registration.")
        
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (user_id, user_name, user_role, password) VALUES (%s, %s, %s, %s)", 
                (user_id, user_name, user_role, user_password)
            )
            conn.commit()
            return User(user_id, user_name, user_role)
        except Exception as e:
            raise DatabaseConnectionError(f"Database connection error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def logout(self):
        log_activity(self.user_id, 'logout')

from data.Database import connect_to_db
from core.Exception import DatabaseConnectionError

class Validation:
    @staticmethod
    def check_menu_item_existence(item_name):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT menu_item_id FROM MenuItems WHERE menu_item_name = %s", (item_name,))
            item_id = cursor.fetchone()
            return bool(item_id)
        except Exception as e:
            raise DatabaseConnectionError(f"Database connection error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

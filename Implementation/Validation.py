from Database import connect_to_db

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
            print(f"An error occurred: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

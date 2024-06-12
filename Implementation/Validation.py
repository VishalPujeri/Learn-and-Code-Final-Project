from Database import *

class Validation:
    @staticmethod
    def check_menu_item_existance(item_name):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT menu_item_id FROM MenuItems WHERE menu_item_name = %s", (item_name,))
        item_id_list = cursor.fetchone()
        if item_id_list:
            return True
        else:
            return False

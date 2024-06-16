from Database import connect_to_db
from User import User
from Cafeteria import MenuItem
from Validation import Validation

class Admin(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Admin')

    def add_menu_item(self, name, price, availability):
        item = MenuItem(None, name, price, availability)
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO MenuItems (menu_item_name, price, availability) VALUES (%s, %s, %s)", 
                       (item.menu_item_name, item.price, item.availability))
        conn.commit()
        conn.close()

    def update_menu_item(self, item_name, item_new_name, price, availability):
        check_item = Validation.check_menu_item_existance(item_name)
        if check_item:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT menu_item_id FROM MenuItems WHERE menu_item_name = %s", (item_name,))
            item_id_list = cursor.fetchone()

            if item_id_list:
                item_id = item_id_list[0]
                cursor.execute(
                    "UPDATE MenuItems SET menu_item_name=%s, price=%s, availability=%s WHERE menu_item_id=%s", 
                    (item_new_name, price, availability, item_id)
                )
                conn.commit()
                conn.close()

    def delete_menu_item(self, item_name):
        check_item = Validation.check_menu_item_existance(item_name)
        if check_item:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MenuItems WHERE menu_item_name = %s", (item_name,))
            conn.commit()
            conn.close()

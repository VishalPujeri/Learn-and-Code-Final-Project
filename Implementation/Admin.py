from Database import connect_to_db
from User import User
from Cafeteria import MenuItem
from Validation import Validation
from notification import add_notification

class Admin(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Admin')

    def add_menu_item(self, name, price, availability):
        item = MenuItem(None, name, price, availability)
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO MenuItems (menu_item_name, price, availability) VALUES (%s, %s, %s)", 
                (item.menu_item_name, item.price, item.availability)
            )
            conn.commit()

            cursor.execute("SELECT user_id FROM Users WHERE user_role = 'Employee'")
            user_ids = cursor.fetchall()
            for user_id in user_ids:
                add_notification(user_id[0], f"New food item added: {name}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def update_menu_item(self, item_name, item_new_name, price, availability):
        try:
            if Validation.check_menu_item_existence(item_name):
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("SELECT menu_item_id FROM MenuItems WHERE menu_item_name = %s", (item_name,))
                item_id = cursor.fetchone()[0]

                cursor.execute(
                    "UPDATE MenuItems SET menu_item_name=%s, price=%s, availability=%s WHERE menu_item_id=%s", 
                    (item_new_name, price, availability, item_id)
                )
                conn.commit()

                cursor.execute("SELECT user_id FROM Users WHERE user_role = 'Employee'")
                user_ids = cursor.fetchall()
                for user_id in user_ids:
                    add_notification(user_id[0], f"Food item updated: {item_name} to {item_new_name} with price {price}")
                return "Food item updated successfully."
            else:
                return "Item not available."
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        finally:
            if 'conn' in locals():
                conn.close()

    def delete_menu_item(self, item_name):
        try:
            if Validation.check_menu_item_existence(item_name):
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM MenuItems WHERE menu_item_name = %s", (item_name,))
                conn.commit()

                cursor.execute("SELECT user_id FROM Users WHERE user_role = 'Employee'")
                user_ids = cursor.fetchall()
                for user_id in user_ids:
                    add_notification(user_id[0], f"Food item deleted: {item_name}")
                return "Food item deleted successfully."
            else:
                return "Item not available."
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        finally:
            if 'conn' in locals():
                conn.close()

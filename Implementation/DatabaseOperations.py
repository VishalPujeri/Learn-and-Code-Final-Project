from Database import connect_to_db
from datetime import datetime
from notification import add_notification

class DatabaseOperations:
    def recommend_menu_items(self, meal_type, number_of_items, item_ids):
        conn = connect_to_db()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        for item_id in item_ids:
            cursor.execute(
                "INSERT INTO Recommendations (menu_item_id, date, meal_type) VALUES (%s, %s, %s)", 
                (item_id, date, meal_type)
            )
        conn.commit()
        cursor.execute("SELECT user_id FROM Users WHERE user_role = 'Employee'")
        user_ids = cursor.fetchall()
        for user_id in user_ids:
            add_notification(user_id[0], "New Menu for today is Rolled out, please click 1 to view")
        conn.close()

    def display_ordered_items(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Orders.menu_item_id, MenuItems.menu_item_name, Orders.order_date, Orders.quantity "
            "FROM Orders "
            "JOIN MenuItems ON Orders.menu_item_id = MenuItems.menu_item_id "
            "WHERE Orders.order_date = CURRENT_DATE"
        )
        ordered_items = cursor.fetchall()
        conn.close()

        display = f"{'Item ID':<10} {'Food Item':<20} {'Quantity':<10}\n" + "-" * 50 + "\n"
        for item in ordered_items:
            display += f"{item[0]:<10} {item[1]:<20} {item[3]:<10}\n"
        return display
    
    def update_profile(self, user_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE UserProfile SET dietary_preference = %s, spice_level = %s, cuisine_preference = %s, sweet_tooth = %s WHERE user_id = %s",
                (dietary_preference, spice_level, cuisine_preference, sweet_tooth, user_id)
            )
            conn.commit()
            return "Profile updated successfully."
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

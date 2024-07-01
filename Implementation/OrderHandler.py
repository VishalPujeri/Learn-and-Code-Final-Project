from Database import connect_to_db
from datetime import datetime

class OrderHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def order_food_item(self, item_id, quantity):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            date = datetime.now().strftime("%Y-%m-%d")

            cursor.execute(
                "SELECT COUNT(*) FROM Recommendations WHERE menu_item_id = %s AND date = %s", 
                (item_id, date)
            )
            recommended_count = cursor.fetchone()[0]
            if recommended_count == 0:
                return "This item is not available in today's recommendations."

            cursor.execute("SELECT price FROM MenuItems WHERE menu_item_id = %s", (item_id,))
            item_data = cursor.fetchone()
            if not item_data:
                return "Invalid item ID."

            price = item_data[0]
            total_price = price * quantity

            cursor.execute(
                "INSERT INTO Orders (user_id, menu_item_id, order_date, quantity, total_price) "
                "VALUES (%s, %s, %s, %s, %s)", 
                (self.user_id, item_id, date, quantity, total_price)
            )
            conn.commit()
            return "Order placed successfully."
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def display_ordered_items(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Orders.menu_item_id, MenuItems.menu_item_name "
                "FROM Orders "
                "JOIN MenuItems ON Orders.menu_item_id = MenuItems.menu_item_id "
                "WHERE Orders.user_id = %s AND Orders.order_date >= DATE_SUB(CURDATE(), INTERVAL 10 DAY)",
                (self.user_id,)
            )
            ordered_items = cursor.fetchall()
            conn.close()

            display = f"{'Item ID':<10} {'Food Item':<20}\n" + "-" * 30 + "\n"
            for item in ordered_items:
                display += f"{item[0]:<10} {item[1]:<20}\n"
            return display
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

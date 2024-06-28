from Database import connect_to_db
from User import User
from datetime import datetime
from Cafeteria import Feedback, UserPreference

class Employee(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Employee')

    def provide_feedback(self, item_id, comment, rating):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Orders WHERE user_id = %s AND menu_item_id = %s", 
                (self.user_id, item_id)
            )
            count = cursor.fetchone()[0]

            if count == 0:
                return "You can only provide feedback for items you have ordered."

            feedback = Feedback(None, item_id, self.user_id, comment, rating, datetime.now())
            cursor.execute(
                "INSERT INTO Feedback (user_id, menu_item_id, comment, rating, feedback_date) "
                "VALUES (%s, %s, %s, %s, %s)", 
                (self.user_id, feedback.menu_item_id, feedback.comment, feedback.rating, feedback.feedback_date)
            )
            conn.commit()
            return "Feedback provided successfully."
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        finally:
            if 'conn' in locals():
                conn.close()

    def select_preference(self, item_id):
        try:
            preference_date = datetime.now().strftime("%Y-%m-%d")
            preference = UserPreference(None, self.user_id, item_id, preference_date)
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO UserPreference (user_id, menu_item_id, preference_date) "
                "VALUES (%s, %s, %s)", 
                (self.user_id, preference.menu_item_id, preference.preference_date)
            )
            conn.commit()
            return "Preference selected successfully."
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

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
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
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
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        
    def submit_detailed_feedback(self, feedback_id, response_1, response_2, response_3):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
        
            cursor.execute(
                "UPDATE DetailedFeedback SET response_1 = %s, response_2 = %s, response_3 = %s WHERE feedback_id = %s",
                (response_1, response_2, response_3, feedback_id)
            )
        
            conn.commit()
            return "Feedback submitted successfully."
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        finally:
            if 'conn' in locals():
                conn.close()


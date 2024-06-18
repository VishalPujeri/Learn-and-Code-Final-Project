from Database import *
from User import *
from Database import connect_to_db

class MenuItem:
    def __init__(self, menu_item_id, menu_item_name, price, availability):
        self.menu_item_id = menu_item_id
        self.menu_item_name = menu_item_name
        self.price = price
        self.availability = availability

class Feedback:
    def __init__(self, feedback_id, menu_item_id, user_id, comment, rating, feedback_date):
        self.feedback_id = feedback_id
        self.menu_item_id = menu_item_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating
        self.feedback_date = feedback_date

class Recommendation:
    def __init__(self, recommendation_id, menu_item_id, date, meal_type):
        self.recommendation_id = recommendation_id
        self.menu_item_id = menu_item_id
        self.date = date
        self.meal_type = meal_type

class UserPreference:
    def __init__(self, preference_id, user_id, menu_item_id,preference_date=None):
        self.preference_id = preference_id
        self.user_id = user_id
        self.menu_item_id = menu_item_id
        self.preference_date = preference_date if preference_date else datetime.now()

class Menu:
    def display_menu_item(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT menu_item_id, menu_item_name, price FROM MenuItems WHERE availability = '1'")
        food_items = cursor.fetchall()
        conn.close()

        display = f"{'Item ID':<10} {'Food Item':<20} {'Price':>10}\n" + "-" * 40 + "\n"
        for food_item in food_items:
            display += f"{food_item[0]:<10} {food_item[1]:<20} {food_item[2]:>10.2f}\n"
        return display

    def display_recommended_menu(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT m.menu_item_id, m.menu_item_name, m.price FROM Recommendations r JOIN MenuItems m ON r.menu_item_id = m.menu_item_id WHERE m.availability = 1 AND date = CURRENT_DATE")
        food_items = cursor.fetchall()
        conn.close()
        
        display = f"{'Item ID':<10} {'Food Item':<20} {'Price':>10}\n" + "-" * 40 + "\n"
        for food_item in food_items:
            display += f"{food_item[0]:<10} {food_item[1]:<20} {food_item[2]:>10.2f}\n"
        return display
    
    
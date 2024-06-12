from Database import *
from User import *

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
    def __init__(self, preference_id, user_id, menu_item_id):
        self.preference_id = preference_id
        self.user_id = user_id
        self.menu_item_id = menu_item_id

class Menu:
    def display_menu_item(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT menu_item_name,price FROM menuitems WHERE availability = '1'")
        food_item = cursor.fetchall()
        conn.close()
        print(f"{'Food Item':<20} {'Price':>10}")
        print("-" * 30)
        for food_items in food_item:
            print(f"{food_items[0]:<20} {food_items[1]:>10.2f}")

    def display_recommended_menu(self):
        conn = connect_to_db()
        cursur = conn.cursor()
        cursur.execute("SELECT m.menu_item_name,m.price FROM recommendations r join menuitems m on r.menu_item_id = m.menu_item_id WHERE m.availability = 1 AND date = CURRENT_DATE")
        food_item = cursur.fetchall()
        conn.close()
        print(f"{'Food Item':<20} {'Price':>10}")
        print("-" * 30)
        for food_items in food_item:
            print(f"{food_items[0]:<20} {food_items[1]:>10.2f}")
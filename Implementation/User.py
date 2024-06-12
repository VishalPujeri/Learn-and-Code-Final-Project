from Database import connect_to_db
from Validation import Validation
from Cafeteria import MenuItem, Feedback, Recommendation, UserPreference, Menu
from datetime import datetime
# from textblob import TextBlob
from Exception import InvalidInputError

class User:
    def __init__(self, user_id, user_name, user_role):
        self.user_id = user_id
        self.user_name = user_name
        self.user_role = user_role

    @staticmethod
    def login(user_id, user_password):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE user_id = %s AND password = %s", (user_id, user_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(user[0], user[1], user[2])
        else:
            return None

class Admin(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Admin')

    def add_menu_item(self):
        name = input("Enter food item name: ")
        while True:
            try:
                price = float(input("Enter food item price: "))
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                availability = int(input("Enter food item availability (1 for available, 0 for not available): "))
                if availability in [0, 1]:
                    break
                else:
                    raise ValueError("Availability must be 1 (available) or 0 (not available).")
            except ValueError as e:
                print(e)

        item = MenuItem(None, name, price, availability)
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO MenuItems (menu_item_name, price, availability) VALUES (%s, %s, %s)", 
                       (item.menu_item_name, item.price, item.availability))
        conn.commit()
        conn.close()
        print("Food item added successfully.")

    def update_menu_item(self):
        item_name = input("Enter food item name to update: ")
        check_item = Validation.check_menu_item_existance(item_name)
        if check_item:
            item_new_name = input("Enter new food item name: ")
            while True:
                try:
                    price = float(input("Enter food item price: "))
                    break
                except ValueError as e:
                    print(e)
            while True:
                try:
                    availability = int(input("Enter food item availability (1 for available, 0 for not available): "))
                    if availability in [0, 1]:
                        break
                    else:
                        raise ValueError("Availability must be 1 (available) or 0 (not available).")
                except ValueError as e:
                    print(e)
        
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
                print("Food item updated successfully.")
            else:
                print("Food item not found.")
        
            conn.close()

        else:
            print("Entered item doesn't exists")

    def delete_menu_item(self):
        item_name = input("Enter the item name to delete: ")
        check_item = Validation.check_menu_item_existance(item_name)
        if check_item:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("Delete from menuitems WHERE menu_item_name = %s",(item_name,))
            conn.commit()
            print("The food item is deleted successfully")
        else:
            print("Entered item doesn't exist")

    @staticmethod
    def register():
        while True:
            user_id = int(input("Enter your user ID to register: "))
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                print("User ID already exists. Please try a different ID.")
            else:
                break
        user_password = input("Enter password")
        user_name = input("Enter your user name: ")
        print("Select role:")
        print("1. Admin  2. Chef  3. Employee")
        role_choice = int(input("Enter the number corresponding to your role: "))
        if role_choice == 1:
            user_role = 'Admin'
        elif role_choice == 2:
            user_role = 'Chef'
        elif role_choice == 3:
            user_role = 'Employee'
        else:
            print("Invalid role choice. Defaulting to Employee.")
            user_role = 'Employee'

        cursor.execute("INSERT INTO Users (user_id, user_name, user_role,password) VALUES (%s, %s, %s, %s)", 
                       (user_id, user_name, user_role, user_password))
        conn.commit()
        conn.close()
        print("Registration successful.")
        return User(user_id, user_name, user_role)

class Chef(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Chef')

    def recommend_menu_items(self):
        items = []
        meal_type = input("Enter meal type (Breakfast, Lunch, Dinner): ")
        number_of_items = int(input("Enter the number of items to recommend: "))
        menu = Menu()
        menu.display_menu_item()
        for _ in range(number_of_items):
            item_id = int(input("Enter food item ID to recommend: "))
            items.append(MenuItem(item_id, None, None, None))
        conn = connect_to_db()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        for item in items:
            cursor.execute("INSERT INTO Recommendations (menu_item_id, date, meal_type) VALUES (%s, %s, %s)", 
                           (item.menu_item_id, date, meal_type))
        conn.commit()
        conn.close()
        print("Menu items recommended successfully.")

    def generate_monthly_feedback_report(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT menu_item_id,comment,rating,feedback_date FROM Feedback WHERE feedback_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()")
        feedbacks = cursor.fetchall()
        conn.close()
        for feedback in feedbacks:
            print(feedback)

class Employee(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Employee')

    def provide_feedback(self):
        item_id = int(input("Enter food item ID to provide feedback: "))
        comment = input("Enter your comment: ")
        while True:
            try:
                rating = float(input("Enter your rating (1-5): "))
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid rating.")
        feedback = Feedback(None, item_id, self.user_id, comment, rating, datetime.now())
        conn = connect_to_db()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Feedback (user_id, menu_item_id, comment, rating, feedback_date) VALUES (%s, %s, %s, %s, %s)", 
                       (self.user_id, feedback.menu_item_id, feedback.comment, feedback.rating, date))
        conn.commit()
        conn.close()
        print("Feedback provided successfully.")

    def select_preference(self):
        item_id = int(input("Enter food item ID to select as preference: "))
        preference = UserPreference(None, self.user_id, item_id)
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO UserPreference (user_id, menu_item_id) VALUES (%s, %s)", 
                       (self.user_id, preference.menu_item_id))
        conn.commit()
        conn.close()
        print("Preference selected successfully.")

    def receive_notification(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Notifications WHERE user_id = %s", (self.user_id,))
        notifications = cursor.fetchall()
        conn.close()
        for notification in notifications:
            print(notification)

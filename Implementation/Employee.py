from Database import connect_to_db
from User import User
from datetime import datetime
from Cafeteria import Feedback, UserPreference

class Employee(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Employee')

    def provide_feedback(self, item_id, comment, rating):
        feedback = Feedback(None, item_id, self.user_id, comment, rating, datetime.now())
        conn = connect_to_db()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Feedback (user_id, menu_item_id, comment, rating, feedback_date) VALUES (%s, %s, %s, %s, %s)", 
                       (self.user_id, feedback.menu_item_id, feedback.comment, feedback.rating, date))
        conn.commit()
        conn.close()

    def select_preference(self, item_id):
        preference_date = datetime.now().strftime("%Y-%m-%d")
        preference = UserPreference(None, self.user_id, item_id, preference_date)
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO UserPreference (user_id, menu_item_id, preference_date) VALUES (%s, %s, %s)", 
                       (self.user_id, preference.menu_item_id, preference.preference_date))
        conn.commit()
        conn.close()
        print("Preference selected successfully.")

    def receive_notification(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT notification_text FROM Notifications WHERE user_id = %s", (self.user_id,))
        notifications = cursor.fetchall()
        cursor.execute("DELETE FROM Notifications WHERE user_id = %s", (self.user_id,))
        conn.commit()
        conn.close()
        return [notification[0] for notification in notifications]

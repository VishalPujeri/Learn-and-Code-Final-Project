from Database import connect_to_db
from datetime import datetime
from Cafeteria import Feedback

class FeedbackHandler:
    def __init__(self, user_id):
        self.user_id = user_id

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
            raise Exception(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

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
            raise Exception(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

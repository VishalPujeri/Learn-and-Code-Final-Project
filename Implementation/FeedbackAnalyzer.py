from Database import connect_to_db
from SentimentAnalyzer import analyze_sentiment
from notification import add_notification
from datetime import datetime

class FeedbackAnalyzer:
    def generate_monthly_report(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT menu_item_id, comment, rating, feedback_date FROM Feedback "
            "WHERE feedback_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()"
        )
        feedbacks = cursor.fetchall()
        conn.close()

        report = f"{'Menu Item ID':<15} {'Comment':<50} {'Rating':<10} {'Feedback Date':<15}\n" + "-" * 90 + "\n"
        for feedback in feedbacks:
            menu_item_id, comment, rating, feedback_date = feedback
            formatted_date = feedback_date.strftime("%Y-%m-%d")
            report += f"{menu_item_id:<15} {comment:<50} {rating:<10} {formatted_date:<15}\n"
        return report

    def view_discard_list(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT menu_item_id, comment, rating FROM Feedback")
        feedback_data = cursor.fetchall()

        if not feedback_data:
            return "No feedback found."

        sentiment_scores = {}
        sentiment_counts = {}
        ratings = {}

        for feedback in feedback_data:
            menu_item_id = feedback[0]
            comment = feedback[1]
            rating = feedback[2]
            sentiment_score = analyze_sentiment(comment)
            if menu_item_id in sentiment_scores:
                sentiment_scores[menu_item_id] += sentiment_score
                sentiment_counts[menu_item_id] += 1
                ratings[menu_item_id].append(rating)
            else:
                sentiment_scores[menu_item_id] = sentiment_score
                sentiment_counts[menu_item_id] = 1
                ratings[menu_item_id] = [rating]

        average_sentiments = {item: sentiment_scores[item] / sentiment_counts[item] for item in sentiment_scores}
        average_ratings = {item: sum(ratings[item]) / len(ratings[item]) for item in ratings}

        combined_scores = {}
        for menu_item_id in average_sentiments:
            sentiment_score = average_sentiments.get(menu_item_id, 0)
            rating = average_ratings.get(menu_item_id, 0)
            combined_score = (sentiment_score + rating) / 2
            combined_scores[menu_item_id] = combined_score

        low_rated_items = {item: score for item, score in combined_scores.items() if score < 2}

        if not low_rated_items:
            return "No low rated items found."

        display = "Low rated items:\n"
        display += f"{'Item ID':<10} {'Average Score':<15}\n" + "-" * 25 + "\n"
        for item_id, avg_score in low_rated_items.items():
            display += f"{item_id:<10} {avg_score:<15.2f}\n"
        display += "Do you want to delete these items? (yes/no): "

        return display

    def roll_out_feedback_request(self, menu_item_id, question_1, question_2, question_3):
        conn = connect_to_db()
        cursor = conn.cursor()
        feedback_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("SELECT user_id FROM Users WHERE user_role = 'Employee'")
        user_ids = cursor.fetchall()

        for user_id in user_ids:
            cursor.execute(
                "INSERT INTO DetailedFeedback (menu_item_id, user_id, question_1, question_2, question_3, feedback_date) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (menu_item_id, user_id[0], question_1, question_2, question_3, feedback_date)
            )
            add_notification(user_id[0], f"We are trying to improve your experience with <Food Item>. Please provide your feedback and help us.\nQ1. {question_1}\nQ2. {question_2}\nQ3. {question_3}")

        conn.commit()
        return "Feedback request rolled out successfully."

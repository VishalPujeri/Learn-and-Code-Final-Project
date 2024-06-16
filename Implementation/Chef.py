from Database import connect_to_db
from User import User
from datetime import datetime
from Cafeteria import MenuItem, Feedback

def analyze_sentiment(comment):
    positive_words = ['good', 'great', 'excellent', 'positive', 'fortunate', 'correct', 'superior', 'amazing', 'happy', 'love', 'like']
    negative_words = ['bad', 'terrible', 'poor', 'negative', 'unfortunate', 'wrong', 'inferior', 'awful', 'sad', 'hate', 'dislike']
    
    words = comment.lower().split()
    sentiment_score = 0
    
    for word in words:
        if word in positive_words:
            sentiment_score += 1
        elif word in negative_words:
            sentiment_score -= 1

    return sentiment_score

class Chef(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Chef')

    def recommend_menu_items(self, meal_type, number_of_items, item_ids):
        conn = connect_to_db()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        for item_id in item_ids:
            cursor.execute("INSERT INTO Recommendations (menu_item_id, date, meal_type) VALUES (%s, %s, %s)", 
                           (item_id, date, meal_type))
        conn.commit()
        conn.close()

    def generate_recommendations_with_preferences(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        # Fetch feedback data
        cursor.execute("SELECT menu_item_id, comment FROM Feedback")
        feedback_data = cursor.fetchall()

        sentiment_scores = {}
        sentiment_counts = {}

        for feedback in feedback_data:
            menu_item_id = feedback[0]
            comment = feedback[1]
            sentiment_score = analyze_sentiment(comment)

            if menu_item_id in sentiment_scores:
                sentiment_scores[menu_item_id] += sentiment_score
                sentiment_counts[menu_item_id] += 1
            else:
                sentiment_scores[menu_item_id] = sentiment_score
                sentiment_counts[menu_item_id] = 1

        average_sentiments = {item: sentiment_scores[item] / sentiment_counts[item] for item in sentiment_scores}

        # Fetch user preferences
        cursor.execute("SELECT menu_item_id, COUNT(*) as preference_count FROM UserPreference GROUP BY menu_item_id")
        preference_data = cursor.fetchall()

        preference_scores = {item[0]: item[1] for item in preference_data}

        # Combine sentiment scores and preference scores
        combined_scores = {}
        for menu_item_id in set(list(average_sentiments.keys()) + list(preference_scores.keys())):
            sentiment_score = average_sentiments.get(menu_item_id, 0)
            preference_score = preference_scores.get(menu_item_id, 0)
            combined_scores[menu_item_id] = sentiment_score + preference_score

        top_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        top_n = 5
        top_n_recommendations = top_recommendations[:top_n]

        # Fetch menu item names
        menu_item_names = {}
        cursor.execute("SELECT menu_item_id, menu_item_name FROM MenuItems")
        menu_items = cursor.fetchall()
        for item in menu_items:
            menu_item_names[item[0]] = item[1]

        # Generate report
        report = "Top Recommended Menu Items based on Feedback Sentiment and User Preferences:\n"
        report += f"{'Menu Item ID':<15} {'Menu Item Name':<25} {'Combined Score':>15}\n" + "-" * 55 + "\n"
        for recommendation in top_n_recommendations:
            menu_item_id = recommendation[0]
            combined_score = recommendation[1]
            menu_item_name = menu_item_names.get(menu_item_id, "Unknown Item")
            report += f"{menu_item_id:<15} {menu_item_name:<25} {combined_score:>15.2f}\n"

        conn.close()
        return report

    def get_recommendations_from_feedback(self):
        return self.generate_recommendations_with_preferences()
    
    def generate_monthly_feedback_report(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT menu_item_id, comment, rating, feedback_date FROM Feedback WHERE feedback_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()")
        feedbacks = cursor.fetchall()
        conn.close()
        report = f"{'Menu Item ID':<15} {'Comment':<50} {'Rating':<10} {'Feedback Date':<15}\n" + "-" * 90 + "\n"
        for feedback in feedbacks:
            menu_item_id, comment, rating, feedback_date = feedback
            formatted_date = feedback_date.strftime("%Y-%m-%d")
            report += f"{menu_item_id:<15} {comment:<50} {rating:<10} {formatted_date:<15}\n"
        return report

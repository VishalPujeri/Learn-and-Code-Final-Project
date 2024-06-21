from Database import connect_to_db
from User import User
from datetime import datetime
from Cafeteria import MenuItem, Feedback
from notification import add_notification

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
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def generate_recommendations_with_preferences(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT menu_item_id, comment, rating FROM Feedback")
            feedback_data = cursor.fetchall()

            sentiment_scores = {}
            sentiment_counts = {}
            ratings = {}

            for feedback in feedback_data:
                menu_item_id = feedback[0]
                comment = feedback[1]
                rating = feedback[2]
                sentiment_score = self.analyze_sentiment(comment)

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

            top_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            top_n = 5
            top_n_recommendations = top_recommendations[:top_n]

            menu_item_names = {}
            cursor.execute("SELECT menu_item_id, menu_item_name FROM MenuItems")
            menu_items = cursor.fetchall()
            for item in menu_items:
                menu_item_names[item[0]] = item[1]

            report = "Top Recommended Menu Items based on Feedback Sentiment and User Preferences:\n"
            report += f"{'Menu Item ID':<15} {'Menu Item Name':<25} {'Combined Score':>15}\n" + "-" * 55 + "\n"

            for recommendation in top_n_recommendations:
                menu_item_id = recommendation[0]
                combined_score = recommendation[1]
                menu_item_name = menu_item_names.get(menu_item_id, "Unknown Item")
                report += f"{menu_item_id:<15} {menu_item_name:<25} {combined_score:>15.2f}\n"
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
        return report

    def analyze_sentiment(self, comment):
        positive_words = ['good', 'great', 'excellent', 'positive', 'fortunate', 'correct', 'superior', 'amazing', 'happy', 'love', 'like']
        negative_words = ['bad', 'terrible', 'poor', 'negative', 'unfortunate', 'wrong', 'inferior', 'awful', 'sad', 'hate', 'dislike']
        
        words = comment.lower().split()
        sentiment_score = 0
        
        for word in words:
            if word in positive_words:
                sentiment_score += 1
            elif word in negative_words:
                sentiment_score -= 1

        max_score = 5
        normalized_sentiment_score = (sentiment_score / max_score) * 5

        normalized_sentiment_score = min(max(normalized_sentiment_score, 0), 5)

        return normalized_sentiment_score

    def get_recommendations_from_feedback(self):
        return self.generate_recommendations_with_preferences()

    def generate_monthly_feedback_report(self):
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")
        return report
    
    def display_ordered_items(self):
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        
    def view_discard_menu_item_list(self):
        try:
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
                sentiment_score = self.analyze_sentiment(comment)  # Ensure analyze_sentiment method is defined

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
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        finally:
            if 'conn' in locals():
                conn.close()

    def delete_menu_item(item_id):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MenuItems WHERE menu_item_id = %s", (item_id,))
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
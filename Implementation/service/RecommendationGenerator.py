from data.Database import connect_to_db
from core.SentimentAnalyzer import analyze_sentiment
from datetime import datetime

class RecommendationGenerator:
    def generate_with_preferences(self):
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

        conn.close()
        return report

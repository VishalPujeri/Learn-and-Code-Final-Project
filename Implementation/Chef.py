from User import User
from DatabaseOperations import DatabaseOperations
from RecommendationGenerator import RecommendationGenerator
from FeedbackAnalyzer import FeedbackAnalyzer
from datetime import datetime

class Chef(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Chef')
        self.db_ops = DatabaseOperations()
        self.recommendation_gen = RecommendationGenerator()
        self.feedback_analyzer = FeedbackAnalyzer()

    def recommend_menu_items(self, meal_type, number_of_items, item_ids):
        try:
            self.db_ops.recommend_menu_items(meal_type, number_of_items, item_ids)
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_recommendations_with_preferences(self):
        try:
            return self.recommendation_gen.generate_with_preferences()
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_monthly_feedback_report(self):
        try:
            return self.feedback_analyzer.generate_monthly_report()
        except Exception as e:
            print(f"An error occurred: {e}")

    def display_ordered_items(self):
        try:
            return self.db_ops.display_ordered_items()
        except Exception as e:
            print(f"An error occurred: {e}")

    def view_discard_menu_item_list(self):
        try:
            return self.feedback_analyzer.view_discard_list()
        except Exception as e:
            print(f"An error occurred: {e}")

    def roll_out_feedback_request(self, menu_item_id, question_1, question_2, question_3):
        try:
            return self.feedback_analyzer.roll_out_feedback_request(menu_item_id, question_1, question_2, question_3)
        except Exception as e:
            print(f"An error occurred: {e}")

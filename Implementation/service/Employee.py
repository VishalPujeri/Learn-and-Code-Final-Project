from core.User import User
from service.FeedbackHandler import FeedbackHandler
from service.PreferenceHandler import PreferenceHandler
from service.OrderHandler import OrderHandler
from data.DatabaseOperations import DatabaseOperations
from core.Cafeteria import Menu
from service.ProfileHandler import ProfileHandler

class Employee(User):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name, 'Employee')
        self.feedback_handler = FeedbackHandler(self.user_id)
        self.preference_handler = PreferenceHandler(self.user_id)
        self.order_handler = OrderHandler(self.user_id)
        self.db_ops = DatabaseOperations()
        self.profile_handler = ProfileHandler(self.user_id)

    def provide_feedback(self, item_id, comment, rating):
        try:
            return self.feedback_handler.provide_feedback(item_id, comment, rating)
        except Exception as e:
            return f"An error occurred: {e}"

    def select_preference(self, item_id):
        try:
            return self.preference_handler.select_preference(item_id)
        except Exception as e:
            return f"An error occurred: {e}"

    def order_food_item(self, item_id, quantity):
        try:
            return self.order_handler.order_food_item(item_id, quantity)
        except Exception as e:
            return f"An error occurred: {e}"

    def display_ordered_items(self):
        try:
            return self.order_handler.display_ordered_items()
        except Exception as e:
            return f"An error occurred: {e}"

    def submit_detailed_feedback(self, feedback_id, response_1, response_2, response_3):
        try:
            return self.feedback_handler.submit_detailed_feedback(feedback_id, response_1, response_2, response_3)
        except Exception as e:
            return f"An error occurred: {e}"

    def update_profile(self, dietary_preference, spice_level, cuisine_preference, sweet_tooth):
        try:
            return self.db_ops.update_profile(self.user_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
        except Exception as e:
            return f"An error occurred: {e}"
        
    def display_recommended_menu(self):
        preferences = self.profile_handler.get_profile_preferences()
        if not preferences:
            return "No preferences found for this user."

        menu = Menu()
        return menu.display_recommended_menu(preferences)

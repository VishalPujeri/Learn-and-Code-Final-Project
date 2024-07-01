from data.Database import connect_to_db
from datetime import datetime
from core.Cafeteria import UserPreference

class PreferenceHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def select_preference(self, item_id):
        try:
            preference_date = datetime.now().strftime("%Y-%m-%d")
            preference = UserPreference(None, self.user_id, item_id, preference_date)
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO UserPreference (user_id, menu_item_id, preference_date) "
                "VALUES (%s, %s, %s)", 
                (self.user_id, preference.menu_item_id, preference.preference_date)
            )
            conn.commit()
            return "Preference selected successfully."
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

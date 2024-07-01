from data.Database import connect_to_db

class ProfileHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_profile_preferences(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT dietary_preference, spice_level, sweet_tooth FROM UserProfile WHERE user_id = %s", (self.user_id,))
            preferences = cursor.fetchone()
            conn.close()
            if preferences:
                return {
                    'dietary_preference': preferences[0],
                    'spice_level': preferences[1],
                    'sweet_tooth': preferences[2]
                }
            else:
                return None
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
from Database import connect_to_db
from Exception import DatabaseConnectionError, NotificationError

def add_notification(user_id, notification_text):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Notifications (user_id, notification_text) VALUES (%s, %s)", 
            (user_id, notification_text)
        )
        conn.commit()
    except Exception as e:
        raise NotificationError(f"Failed to add notification: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_notifications(user_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT notification_text FROM Notifications WHERE user_id = %s", (user_id,))
        notifications = cursor.fetchall()
        cursor.execute("DELETE FROM Notifications WHERE user_id = %s", (user_id,))
        conn.commit()
        return [notification[0] for notification in notifications]
    except Exception as e:
        raise NotificationError(f"Failed to get notifications: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

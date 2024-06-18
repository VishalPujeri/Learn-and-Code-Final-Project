from Database import connect_to_db

def add_notification(user_id, notification):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Notifications (user_id, notification_text) VALUES (%s, %s)", (user_id, notification))
    conn.commit()
    conn.close()

def get_notifications(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT notification_text FROM Notifications WHERE user_id = %s", (user_id,))
    notifications = cursor.fetchall()
    cursor.execute("DELETE FROM Notifications WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()
    
    return [notification[0] for notification in notifications]

from datetime import datetime

LOG_FILE = 'user_activity_log.txt'

def log_activity(user_id, action):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f'{timestamp} - User ID: {user_id} - Action: {action}\n')

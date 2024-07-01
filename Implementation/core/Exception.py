class CafeteriaError(Exception):
    pass

class DatabaseConnectionError(CafeteriaError):
    def __init__(self, message="Error connecting to the database"):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(CafeteriaError):
    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)

class ItemNotFoundError(CafeteriaError):
    def __init__(self, item_name=""):
        self.message = f"Item '{item_name}' not found."
        super().__init__(self.message)

class UserNotAuthorizedError(CafeteriaError):
    def __init__(self, message="User not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)

class NotificationError(CafeteriaError):
    def __init__(self, message="Failed to send notification"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    def __init__(self, message="Requested User not found."):
        super().__init__(message)

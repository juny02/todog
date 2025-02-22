class MealRecordNotFoundError(Exception):
    def __init__(self, message="Requested MealRecord not found."):
        super().__init__(message)

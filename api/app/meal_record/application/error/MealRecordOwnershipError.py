class MealRecordOwnershipError(Exception):
    def __init__(self, message="MealRecord does not belong to requested Dog."):
        super().__init__(message)
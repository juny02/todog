class DogFamilyNotFoundError(Exception):
    def __init__(self, message="Requested DogFamily relationship not found."):
        super().__init__(message)

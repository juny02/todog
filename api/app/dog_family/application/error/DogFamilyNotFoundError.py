class DogFamilyNotFoundError(Exception):
    def __init__(self, message="Requested relation not found."):
        super().__init__(message)

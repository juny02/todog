class DogNotFoundError(Exception):
    def __init__(self, message="Requested Dog not found."):
        super().__init__(message)

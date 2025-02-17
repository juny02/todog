class DogFamilyAlreadyExistsError(Exception):
    def __init__(self, message="DogFamily relationship already exists."):
        super().__init__(message)

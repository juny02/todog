class TreatNotFoundError(Exception):
    def __init__(self, message="Requested Treat not found."):
        super().__init__(message)

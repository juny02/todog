class MedRecordNotFoundError(Exception):
    def __init__(self, message="Requested MedRecord not found."):
        super().__init__(message)

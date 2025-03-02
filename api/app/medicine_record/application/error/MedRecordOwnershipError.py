class MedRecordOwnershipError(Exception):
    def __init__(self, message="MedRecord does not belong to requested Dog."):
        super().__init__(message)
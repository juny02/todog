class TreatRecordOwnershipError(Exception):
    def __init__(self, message="TreatRecord does not belong to requested Dog."):
        super().__init__(message)
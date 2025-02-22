class WalkRecordOwnershipError(Exception):
    def __init__(self, message="WalkRecord does not belong to requested Dog."):
        super().__init__(message)
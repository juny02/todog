class WalkRecordNotFoundError(Exception):
    def __init__(self, message="Requested WalkRecord not found."):
        super().__init__(message)

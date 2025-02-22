class TreatRecordNotFoundError(Exception):
    def __init__(self, message="Requested TreatRecord not found."):
        super().__init__(message)

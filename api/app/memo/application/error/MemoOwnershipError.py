class MemoOwnershipError(Exception):
    def __init__(self, message="Memo does not belong to requested Dog."):
        super().__init__(message)
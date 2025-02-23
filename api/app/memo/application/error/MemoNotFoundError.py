class MemoNotFoundError(Exception):
    def __init__(self, message="Requested Memo not found."):
        super().__init__(message)

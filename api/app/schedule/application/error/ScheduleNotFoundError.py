class ScheduleNotFoundError(Exception):
    def __init__(self, message="Requested Schedule not found."):
        super().__init__(message)

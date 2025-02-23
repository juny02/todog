class ScheduleOwnershipError(Exception):
    def __init__(self, message="Schedule does not belong to requested Dog."):
        super().__init__(message)
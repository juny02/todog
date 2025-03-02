class MedScheduleNotFoundError(Exception):
    def __init__(self, message="Requested MedSchedule not found."):
        super().__init__(message)

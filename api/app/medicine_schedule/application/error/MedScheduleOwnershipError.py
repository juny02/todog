class MedScheduleOwnershipError(Exception):
    def __init__(self, message="MedSchedule does not belong to requested Dog."):
        super().__init__(message)
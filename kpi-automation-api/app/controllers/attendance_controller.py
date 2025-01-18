from app.services.attendance_service import AttendanceService

class AttendanceController:
    """
    Handles attendance-related operations.

    Provides a static method for creating attendance records by
    delegating the responsibility to the AttendanceService. This
    class centralizes attendance management functions.

    """
    @staticmethod
    def create_attendance(data):
            return AttendanceService.create_attendance(data)

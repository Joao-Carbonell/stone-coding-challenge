from flask import make_response, jsonify
from marshmallow import ValidationError

from app.schemas.attendance_schema import AttendanceSchema
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
        """
        Creates an attendance record for the given input data by utilizing
        the AttendanceService.

        This method is responsible for interacting with the AttendanceService
        to create a new attendance record. It accepts the necessary input data
        and delegates the creation logic to the service.

        :param data: The input data required to create an attendance record.
        :type data: Any
        :return: The result of the attendance creation operation
                 as processed by the AttendanceService.
        :rtype: Any
        """
        return AttendanceService.create_attendance(data)

    @staticmethod
    def update_attendance(data, id):
        """
        Updates attendance records for a specific user.

        This method takes in attendance data and an identifier, validates the data using the
        `AttendanceSchema`, and updates attendance records by utilizing the
        `AttendanceService.update_attendance` function. If validation fails or other exceptions arise,
        appropriate error responses are returned.

        :param data: A dictionary containing attendance update data to be validated.
        :param id: An identifier for the user whose attendance is to be updated.
        :return: An HTTP response object. On success, returns the updated attendance data.
            On failure, returns an error message with a corresponding HTTP status code.
        """

        return AttendanceService.update_attendance(data, id)



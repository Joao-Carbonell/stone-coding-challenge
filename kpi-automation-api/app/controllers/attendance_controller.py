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
        try:
            schema = AttendanceSchema()
            # Validating the data sent from the client
            validated_data = schema.load(data)
            # Sending data to the service
            return AttendanceService.update_attendance(validated_data, id)
        except ValidationError as ve:
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except Exception as e:
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_FOUND', 'error': str(e)}), 500)

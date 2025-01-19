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
        try:
            schema = AttendanceSchema()
            validated_data = schema.load(data)
            return AttendanceService.update_attendance(validated_data, id)
        except ValidationError as ve:
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except Exception as e:
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_FOUND', 'error': str(e)}), 500)

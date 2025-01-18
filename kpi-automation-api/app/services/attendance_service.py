from flask import jsonify, make_response
from app.schemas.attendance_schema import AttendanceSchema
from app.models.attendance.attendance_model import Attendance
from app.config.config import db
from marshmallow import ValidationError


class AttendanceService:
    @staticmethod
    def create_attendance(data):
        """
        Creates a new attendance record after validating input data using a schema, adding
        the validated object to the database session, and committing the session. Handles
        possible validation and operational errors during the process.

        :param data: Dictionary containing the data required to create an attendance record.
        :return: A Flask response object with a message and HTTP status code. Possible
                 responses include:
                 - {'message': 'ATTENDANCE_CREATED'}, 201: Successfully created the
                   attendance.
                 - {'message': 'INVALID_DATA', 'errors': <validation_error_messages>}, 400:
                   Input data failed validation checks.
                 - {'message': 'ATTENDANCE_NOT_CREATED', 'error': <error_message>}, 500:
                   An unexpected error occurred while creating the attendance.
        """
        schema = AttendanceSchema()
        try:
            # Uses the schema validator to validate the data
            validated_data = schema.load(data)
            new_attendance = Attendance(**validated_data)

            #Place an object into the db session
            db.session.add(new_attendance)
            # Commit the db changes
            db.session.commit()


            return make_response(jsonify({'message': 'ATTENDANCE_CREATED'}), 201)
        except ValidationError as ve:
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_CREATED', 'error': str(e)}), 500)
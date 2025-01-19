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

            # TODO: replace the return by:
            #  return make_response(jsonify({'message': 'ATTENDANCE_CREATED', 'attendance': new_attendance.to_dict()}), 201)
            return make_response(jsonify({'message': 'ATTENDANCE_CREATED'}), 201)
        except ValidationError as ve:
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_CREATED', 'error': str(e)}), 500)

    @staticmethod
    def update_attendance(data, id):
        """
        Updates an attendance record with the provided data for a specified ID.

        This method retrieves an attendance record by its ID, updates its attributes
        based on the provided data, commits the changes to the database, and returns
        a JSON response containing the updated attendance record.

        :param data: Dictionary containing key-value pairs to update in the attendance record
        :type data: dict
        :param id: Unique identifier of the attendance record to update
        :type id: int
        :raises ValueError: If the attendance record with the specified ID is not found
        :return: A tuple containing a JSON representation of the updated
                 attendance record and an HTTP status code of 200
        :rtype: tuple
        """
        # Retrieve the attendance by id
        attendance_record = Attendance.query.get(id)

        # Verify if the attendance exists
        if not attendance_record:
            # If not raise an error
            raise ValueError(f"ATTENDANCE_NOT_FOUND")

        # Update the attendance attributes in a mapped list
        list(map(lambda kv: setattr(attendance_record, kv[0], kv[1]), data.items()))

        db.session.commit()

        return jsonify({"attendance": attendance_record.to_dict()}), 200
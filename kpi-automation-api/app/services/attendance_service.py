from flask import jsonify, make_response
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from app.dto.attendance import AttendanceCreationSchema
from app.models.attendance.attendance_model import Attendance
from app.config.config import db
from marshmallow import ValidationError

"""
    Service for creating and updating attendance records.

    Methods:
        create_attendance: Validates input and creates a new attendance record.
        update_attendance: Updates an existing attendance record by ID.
    """
class AttendanceService:

    @staticmethod
    def create_attendance(data):
        attendance_creation_schema = AttendanceCreationSchema()
        try:
            # Uses the schema validator to validate the data
            validated_data = attendance_creation_schema.load(data)
            # Create a new Attendance object
            new_attendance = Attendance(id_attendance = validated_data.id_attendance,
                                           id_client = validated_data.id_client,
                                           angel = validated_data.angel,
                                           pole = validated_data.pole,
                                           deadline = validated_data.deadline,
                                           attendance_date = validated_data.attendance_date)

            # Execute a transaction to db
            db.session.execute(
                insert(Attendance).values(id_attendance = new_attendance.id_attendance,
                                           id_client = new_attendance.id_client,
                                           angel = new_attendance.angel,
                                           pole = new_attendance.pole,
                                           deadline = new_attendance.deadline,
                                           attendance_date = new_attendance.attendance_date)
            )
            # Commit the db changes
            db.session.commit()

            return make_response(jsonify({'message': 'ATTENDANCE_CREATED', 'attendance': new_attendance.to_dict()}), 201)
        except ValidationError as ve:
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'DATABASE_ERROR', 'error': str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_CREATED', 'error': str(e)}), 500)

    @staticmethod
    def update_attendance(data, id):

        attendance_creation_schema = AttendanceCreationSchema()
        try:
            if not id or not isinstance(id, int):
                raise ValueError("Invalid attendance ID")
            # Uses the schema validator to validate the data
            # Using db.session.query due the Attendance.query.get are deprecated
            attendance_record = db.session.query(Attendance).filter(Attendance.id == id).one()

            validated_data = attendance_creation_schema.load(data)

            attendance_record.attendance = validated_data

            # Place an object into the db session
            db.session.execute(
                insert(Attendance).values(id_attendance=attendance_record.id_attendance,
                                          id_client=attendance_record.id_client,
                                          angel=attendance_record.angel,
                                          pole=attendance_record.pole,
                                          deadline=attendance_record.deadline,
                                          attendance_date=attendance_record.attendance_date)
            )
            # Commit the db changes
            db.session.commit()

            return make_response(jsonify({'message': 'ATTENDANCE_UPDATED'}), 201)
        except ValidationError as ve:
            db.session.rollback()
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'DATABASE_ERROR', 'errors': str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_UPDATED', 'error': str(e)}), 500)

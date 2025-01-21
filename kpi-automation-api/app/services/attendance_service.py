from flask import jsonify, make_response
from sqlalchemy import insert, select, desc
from sqlalchemy.exc import SQLAlchemyError
from app.dto.attendance import AttendanceCreationSchema
from app.models.attendance.attendance_model import Attendance
from app.config.config import db
from marshmallow import ValidationError

from app.repositories.attendance_repository import AttendanceRepository
from app.schemas.attendance_schema import AttendanceSchema
from app.utils.date_utils import parse_date
"""
    Service for creating and updating attendance records.

    Methods:
        create_attendance: Validates input and creates a new attendance record.
        update_attendance: Updates an existing attendance record by ID.
    """
class AttendanceService:
    # TODO: Remove database queries from service and move to repository
    @staticmethod
    def create_attendance(data):
        attendance_creation_schema = AttendanceCreationSchema()
        try:
            # Uses the schema validator to validate the data
            # @TODO: Remove validations from services
            validated_data = attendance_creation_schema.load(data)
            #  Using the attendance repository to create an attendance register on db
            new_attendance = AttendanceRepository.create_attendance(validated_data)

            return make_response(jsonify({'message': 'ATTENDANCE_CREATED', 'attendance': new_attendance.to_dict()}), 201)
        except ValidationError as ve:
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'DATABASE_ERROR', 'error': str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_CREATED', 'error': str(e)}), 500)

    # TODO: Remove database queries from service and move to repository
    @staticmethod
    def update_attendance(data, id):

        attendance_creation_schema = AttendanceCreationSchema()
        try:
            # Using the attendance repository to find an attendance register on db
            attendance_record = AttendanceRepository.get_attendance_by_id(id)

            # @TODO: Remove validations from services
            # Uses the schema validator to validate the data
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

    # TODO: Remove database queries from service and move to repository
    @staticmethod
    def retrieve_attendance(id):

        attendance_schema = AttendanceSchema()
        try:
            # Uses the schema validator to validate the data
            attendance = attendance_schema.dump(AttendanceRepository.get_attendance_by_id(id))

            return make_response(jsonify({'message': 'ATTENDANCE_FOUND', 'attendance': attendance}), 201)
        except ValidationError as ve:
            db.session.rollback()
            return make_response(jsonify({'message': 'INVALID_DATA', 'errors': ve.messages}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'DATABASE_ERROR', 'errors': str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'ATTENDANCE_NOT_FOUND', 'error': str(e)}), 500)

    # TODO: Remove database queries from service and move to repository
    @staticmethod
    def get_all_attendances(args):

        query = AttendanceRepository.get_attendances()

        id_client = args.get('id_client')
        id_attendance = args.get('id_attendance')
        deadline = ""
        attendance_date = ""

        if args.get('deadline'):
            deadline = parse_date(args.get('deadline'))

        pole = args.get('pole')

        if args.get('attendance_date'):
            attendance_date = parse_date(args.get('attendance_date'))

        angel = args.get('angel')
        sorts = args.get('sort')
        filter_map = {
            'id_client': lambda q, v: q.filter(Attendance.id_client.ilike(f"%{v}%")) if v else q,
            'attendance_date': lambda q, v: q.filter(
                Attendance.attendance_date.between(attendance_date, deadline)) if attendance_date and deadline else (
                q.filter(Attendance.attendance_date >= attendance_date) if attendance_date else q.filter(
                    Attendance.attendance_date <= deadline) if deadline else q
            ),
            'deadline': lambda q, v: q.filter(
                Attendance.attendance_date.between(deadline, attendance_date)) if deadline and attendance_date else (
                q.filter(Attendance.deadline >= deadline) if deadline else q.filter(
                    Attendance.deadline <= attendance_date) if deadline else q
            ),
            'pole': lambda q, v: q.filter(Attendance.pole == v) if v else q,
            'angel': lambda q, v: q.filter(Attendance.angel == v) if v else q,
            'id_attendance': lambda q, v: q.filter(Attendance.id_attendance == v) if v else q
        }

        if id_client:
            query = filter_map['id_client'](query, id_client)
        if id_attendance:
            query = filter_map['id_attendance'](query, id_attendance)
        if pole:
            query = filter_map['pole'](query, pole)
        if attendance_date:
            query = filter_map['attendance_date'](query, attendance_date)
        if deadline:
            query = filter_map['deadline'](query, deadline)
        if angel:
            query = filter_map['angel'](query, angel)

        if sorts:
            for sort in sorts.split(","):
                descending = sort[0] == "-"
                if descending:
                    field = getattr(Attendance, sort[1:])
                    query = query.order_by(desc(field))
                else:
                    field = getattr(Attendance, sort)
                    query = query.order_by(field)

        attendances = query.all()
        schema = AttendanceSchema(many=True)
        result = schema.dump(attendances)
        return jsonify(result)



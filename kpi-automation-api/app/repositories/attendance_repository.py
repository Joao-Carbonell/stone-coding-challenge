from sqlalchemy import func, select, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import case

from app.config.config import db
from app.models.attendance.attendance_model import Attendance


class AttendanceRepository:

    @staticmethod
    def create_attendance(validated_data):
        """
        Creates a new attendance record in the database using the provided validated
        data. This method ensures that no unnecessary or system-managed fields are
        included during the creation of the new record. It handles database exceptions
        to maintain transactional integrity.

        :param validated_data: A dictionary containing the validated data for
            creating the attendance record. If the provided data is not a dictionary,
            it attempts to convert it to a dictionary using `to_dict`.
        :return: The newly created `Attendance` object.
        :rtype: Attendance
        :raises SQLAlchemyError: If there is an error during the database operation.
        :raises Exception: For any other non-database related errors.
        """
        try:
            if not isinstance(validated_data, dict):
                validated_data = validated_data.to_dict()

            # Blah! Refactor this
            # TODO: Refactor
            validated_data.pop('id', None)
            validated_data.pop('created_at', None)
            validated_data.pop('updated_at', None)
            new_attendance = Attendance(**validated_data)

            db.session.add(new_attendance)

            db.session.commit()

            return new_attendance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise e
    # Returning a simple register of Attendance on db
    @staticmethod
    def get_attendances():
        """
        Fetches all attendance records from the database.

        This method queries the database for all records in the Attendance table and returns
        the results as a query object. It is implemented as a static method, not requiring any
        instance of the class to be called.

        :return: Query object containing all attendance records.
        :rtype: sqlalchemy.orm.query.Query
        """
        return db.session.query(Attendance)

    # Returning all registers of Attendance on db
    @staticmethod
    def get_attendance_by_id(id):
        """
        Retrieves the attendance record corresponding to the given ID.

        This function fetches an attendance record by its unique identifier using
        a database query. It ensures that only a single, specific record is
        retrieved or throws an exception if not successful.

        :param id: The unique identifier of the attendance record to retrieve
        :type id: int
        :return: A single attendance record matching the specified ID
        :rtype: Attendance
        :raises sqlalchemy.orm.exc.NoResultFound: If no attendance record is found for the specified ID
        :raises sqlalchemy.orm.exc.MultipleResultsFound: If multiple attendance records are found
        """
        # Using db.session.query due the Attendance.query.get are deprecated
        return db.session.scalars(select(Attendance).where(Attendance.id == id)).one()

    # Returning a list of registers of Attendance on db by a period of time
    @staticmethod
    def get_attendances_by_period(start_date, end_date):
        """
        Fetches the total attendance for each angel within a given date range. This method
        queries the database to count the attendance records, groups them by the angel,
        and returns the results. It is a static method designed to operate without
        requiring an instance of the containing class.

        :param start_date: The start date of the period to filter attendance records.
            The date must be provided in a valid format recognized by the database.
        :param end_date: The end date of the period to filter attendance records.
            The date must be provided in a valid format recognized by the database.
        :return: A list of tuples where each tuple consists of an angel object and the
            corresponding count of attendance records for the specified period.
            Example format: [(angel1, total_attendance1), (angel2, total_attendance2), ...]
        :rtype: list[tuple[Angel, int]]
        """
        return (db.session.query(
            Attendance.angel,
            func.count(Attendance.id).label('total_attendances'),
            func.min(Attendance.attendance_date).label('start_date'),
            func.max(Attendance.attendance_date).label('end_date')
        ).filter(
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        ).group_by(Attendance.angel).all())

    @staticmethod
    def get_productivity_by_angel(angel):

        query = db.session.query(
            Attendance.angel,
            func.count(Attendance.id).label('total_attendances'),
            func.min(Attendance.attendance_date).label('start_date'),
            func.max(Attendance.attendance_date).label('end_date'),
            func.sum(
                case(
                    (Attendance.attendance_date <= Attendance.deadline, 1),
                    else_=0
                )
            ).label('on_time_attendances')
        ).filter(Attendance.angel == angel)

        return query.group_by(Attendance.angel).all()
    # Returning a list of registers of Attendance on db by a period of time by a angel
    @staticmethod
    def get_productivity_by_period_with_angel(start_date, end_date, angel):
        """
        Fetches the productivity data of a specific "angel" over a given time period. The
        productivity is calculated based on the total attendance count within the
        specified date range.

        :param start_date: The start date of the period to filter attendances (inclusive).
        :type start_date: datetime.date
        :param end_date: The end date of the period to filter attendances (inclusive).
        :type end_date: datetime.date
        :param angel: The identifier of the "angel" for which productivity data is to be
            retrieved.
        :type angel: str
        :return: A list of results containing the "angel" and their corresponding total
            attendance count within the given period.
        :rtype: list[tuple[str, int]]
        """
        query = db.session.query(
            Attendance.angel,
            func.count(Attendance.id).label('total_attendances')
        ).filter(
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        )
        query = query.filter(Attendance.angel == angel)

        return query.group_by(Attendance.angel).all()

    # Querying productivity of a pole on db in a period
    @staticmethod
    def get_productivity_by_logistics_pole_and_period(pole, start_date, end_date):
        """
        Fetches productivity metrics for a specific logistics pole within a defined time period by querying the attendance data. This includes total attendances and the count of on-time attendances.

        :param pole: The logistics pole for which the productivity data is to be computed
        :type pole: str
        :param start_date: The start date of the period for filtering attendance records
        :type start_date: datetime.date
        :param end_date: The end date of the period for filtering attendance records
        :type end_date: datetime.date
        :return: A list of grouped query results containing logistics pole, total attendances, and on-time attendances
        :rtype: list
        """
        # Query to count the attendances on time in a pole
        query = db.session.query(
            Attendance.pole,
            func.count(Attendance.id).label('total_attendances'),
            func.sum(
                case(
                    (Attendance.attendance_date <= Attendance.deadline, 1),
                    else_=0
                )
            ).label('on_time_attendances')
        ).filter(
            Attendance.pole == pole,
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        )

        return query.group_by(Attendance.pole).all()


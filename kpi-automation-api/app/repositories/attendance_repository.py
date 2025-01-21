from sqlalchemy import func, select
from sqlalchemy.sql import case

from app.config.config import db
from app.models.attendance.attendance_model import Attendance


class AttendanceRepository:

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
            func.count(Attendance.id).label('total_attendance')
        ).filter(
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        ).group_by(Attendance.angel).all())

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
            func.count(Attendance.id).label('total_attendance')
        ).filter(
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        )
        query = query.filter(Attendance.angel == angel)

        return query.group_by(Attendance.angel).all()

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
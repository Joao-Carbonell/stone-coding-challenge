from datetime import datetime
from app.config.config import db


#TODO: Add python documentation
class Attendance(db.Model):
    """
    Represents the attendance records with relevant metadata.

    This class is designed for handling attendance records including details about
    the client, associated angel, pole, and significant dates such as deadline and
    attendance date. It includes validation for attribute assignments and ensures
    that data integrity is maintained. It is a SQLAlchemy model, hence linked with a
    backend database.

    :ivar _id: Unique identifier for the attendance record.
    :type _id: int
    :ivar _id_attendance: External attendance identifier.
    :type _id_attendance: int
    :ivar _id_client: Unique identifier of the associated client.
    :type _id_client: int
    :ivar _angel: Description or identifier of the angel in the context of the attendance.
    :type _angel: str
    :ivar _pole: Description or identifier of the pole in the context of the attendance.
    :type _pole: str
    :ivar _deadline: Deadline datetime for the attendance record.
    :type _deadline: datetime
    :ivar _attendance_date: Date and time of the attendance record.
    :type _attendance_date: datetime
    """
    __tablename__ = 'attendances'

    _id = db.Column(db.Integer, primary_key=True)
    _id_attendance = db.Column('id_attendance', db.Integer)
    _id_client = db.Column('id_client', db.Integer, nullable=False)
    _angel = db.Column('angel', db.String(255), nullable=False)
    _pole = db.Column('pole', db.String(255), nullable=False)
    _deadline = db.Column('deadline', db.DateTime, nullable=False)
    _attendance_date = db.Column('attendance_date', db.DateTime, nullable=False)

    def __init__(self, id_attendance, id_client, angel, pole, deadline, attendance_date):
        self.id_attendance = id_attendance
        self.id_client = id_client
        self.angel = angel
        self.pole = pole
        self.deadline = deadline
        self.attendance_date = attendance_date

    @property
    def id_attendance(self):
        return self._id_attendance

    @id_attendance.setter
    def id_attendance(self, value):
        if isinstance(value, int) and value > 0:
            self._id_attendance = value
        else:
            raise ValueError("INVALID_ATTENDANCE_ID") #

    @property
    def id_client(self):
        return self._id_client

    @id_client.setter
    def id_client(self, value):
        if isinstance(value, int) and value > 0:
            self._id_client = value
        else:
            raise ValueError("INVALID_CLIENT_ID")

    @property
    def angel(self):
        return self._angel

    @angel.setter
    def angel(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._angel = value
        else:
            raise ValueError("EMPTY_STRING_FOR_ANGEL_NAME")

    @property
    def pole(self):
        return self._pole

    @pole.setter
    def pole(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._pole = value
        else:
            raise ValueError("EMPTY_STRING_FOR_POLE_NAME")

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        if isinstance(value, datetime):
            self._deadline = value
        else:
            raise ValueError("DEADLINE_DATETIME_INVALID")

    @property
    def attendance_date(self):
        return self._attendance_date

    @attendance_date.setter
    def attendance_date(self, value):
        if isinstance(value, datetime):
            self._attendance_date = value
        else:
            raise ValueError("ATTENDANCE_DATETIME_INVALID")

    def __repr__(self):
        return f"<Attendance {self.id_attendance} - {self.angel} - {self.pole}>"

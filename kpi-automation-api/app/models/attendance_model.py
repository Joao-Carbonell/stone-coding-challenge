from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#TODO: Add python documentation
class Attendance(db.Model):
    __tablename__ = 'attendances'

    # TODO: Add python documentation
    id_attendance = db.Column(db.Integer, primary_key=True)
    _id_client = db.Column('id_client', db.Integer, nullable=False)
    _green_angel = db.Column('angel', db.String(255), nullable=False)
    _pole = db.Column('pole', db.String(255), nullable=False)
    _deadline = db.Column('deadline', db.Date, nullable=False)
    _attendance_date = db.Column('attendance_date', db.DateTime, nullable=False)

    #TODO: Add python documentation
    def __init__(self, id_client, angel, pole, deadline, attendance_date):
        self.id_client = id_client
        self.angel = angel
        self.pole = pole
        self.deadline = deadline
        self.attendance_date = attendance_date

    # TODO: Add python documentation
    @property
    def id_client(self):
        return self._id_client

    # TODO: Add python documentation
    @id_client.setter
    def id_client(self, value):
        if isinstance(value, int) and value > 0:
            self._id_client = value
        else:
            raise ValueError("INVALID_CLIENT_ID")

    # TODO: Add python documentation
    @property
    def angel(self):
        return self._green_angel

    # TODO: Add python documentation
    @angel.setter
    def angel(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._green_angel = value
        else:
            raise ValueError("EMPTY_STRING_FOR_ANGEL_NAME")

    # TODO: Add python documentation
    @property
    def pole(self):
        return self._pole

    # TODO: Add python documentation
    @pole.setter
    def pole(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._pole = value
        else:
            raise ValueError("EMPTY_STRING_FOR_POLE_NAME")

    # TODO: Add python documentation
    @property
    def deadline(self):
        return self._deadline

    # TODO: Add python documentation
    @deadline.setter
    def deadline(self, value):
        if isinstance(value, datetime):
            self._deadline = value
        else:
            raise ValueError("DEADLINE_DATETIME_INVALID")

    # TODO: Add python documentation
    @property
    def attendance_date(self):
        return self._attendance_date

    @attendance_date.setter
    def attendance_date(self, value):
        if isinstance(value, datetime):
            self._attendance_date = value
        else:
            raise ValueError("ATTENDANCE_DATETIME_INVALID")

    # TODO: Add python documentation
    def __repr__(self):
        return f"<Attendance {self.id_attendance} - {self.angel} - {self.pole}>"

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

    #@TODO: Replace id by uuid
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    id_attendance = db.Column('id_attendance', db.Integer)
    id_client = db.Column('id_client', db.Integer, nullable=False)
    angel = db.Column('angel', db.String(255), nullable=False)
    pole = db.Column('pole', db.String(255), nullable=False)
    deadline = db.Column('deadline', db.DateTime, nullable=False)
    attendance_date = db.Column('attendance_date', db.DateTime, nullable=False)

    def __init__(self, id_attendance, id_client, angel, pole, deadline, attendance_date):
        self.id_attendance = id_attendance
        self.id_client = id_client
        self.angel = angel
        self.pole = pole
        self.deadline = deadline
        self.attendance_date = attendance_date

    def __repr__(self):
        return (f"<Attendance { self.id } - {self.id_attendance} - {self.id_client} - {self.angel} - {self.pole} - "
                f"{self.attendance_date} - {self.deadline}>")

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "id_attendance": self.id_attendance,
            "id_client": self.id_client,
            "angel" : self.angel,
            "pole": self.pole,
            "attendance_date": self.attendance_date,
            "deadline": self.deadline,
        }

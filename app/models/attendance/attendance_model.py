from datetime import datetime
from app.config.config import db


#TODO: Add python documentation
class Attendance(db.Model):
    """
    Represents the Attendance model, which encapsulates data about a single attendance record.

    This class defines the database schema for the `attendances` table and provides methods for
    representation, serialization, and creation of attendance instances from CSV data. The class
    serves as the core model for managing attendance-related operations, and all attributes align
    with the database fields.

    :ivar id: Primary key for the attendance record.
    :type id: int
    :ivar created_at: Timestamp when the attendance record was created.
    :type created_at: datetime
    :ivar updated_at: Timestamp when the attendance record was last updated.
    :type updated_at: datetime
    :ivar id_attendance: Unique identifier for the attendance instance, provided externally.
    :type id_attendance: int
    :ivar id_client: Identifier for the api_client associated with the attendance.
    :type id_client: int
    :ivar angel: Name of the associated angel (representative).
    :type angel: str
    :ivar pole: Name of the associated pole or center.
    :type pole: str
    :ivar deadline: The deadline assigned to the attendance.
    :type deadline: datetime
    :ivar attendance_date: The date on which the attendance occurred, if applicable.
    :type attendance_date: datetime or None
    """
    __tablename__ = 'attendances'

    #@TODO: Replace id by uuid
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    id_attendance = db.Column('id_attendance', db.Integer, nullable=False)
    id_client = db.Column('id_client', db.Integer, nullable=False)
    angel = db.Column('angel', db.String(255), nullable=False)
    pole = db.Column('pole', db.String(255), nullable=False)
    deadline = db.Column('deadline', db.DateTime, nullable=False)
    attendance_date = db.Column('attendance_date', db.DateTime, nullable=True)

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
    @staticmethod
    def create_from_csv(csv_row):
        return Attendance(
            id_attendance=csv_row['id_atendimento'],
            id_client=csv_row['id_cliente'],
            angel=csv_row['angel'],
            pole=csv_row['polo'],
            deadline=csv_row['data_limite'],
            attendance_date=csv_row.get('data_de_atendimento')
        )
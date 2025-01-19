from marshmallow import Schema, fields, ValidationError, pre_load
from app.utils.date_utils import parse_date


class AttendanceSchema(Schema):
    """
    Schema definition for attendance data.

    The AttendanceSchema class defines the structure of data related to attendance.
    It specifies required fields, their types, and serializing/deserializing
    functions for date fields. This schema ensures proper validation and
    transformation of attendance data.

    :ivar id_attendance: Unique identifier for the attendance record.
    :type id_attendance: int
    :ivar id_client: Identifier for the client associated with the attendance.
    :type id_client: int
    :ivar angel: Name or identifier of the associated angel.
    :type angel: str
    :ivar pole: Name or location of the pole associated with the attendance.
    :type pole: str
    :ivar deadline: Deadline date for the attendance, with custom serialization
        and deserialization logic.
    :type deadline: Function
    :ivar attendance_date: Date of the attendance event, with custom serialization
        and deserialization logic.
    :type attendance_date: Function
    """
    id_attendance = fields.Int(required=True)
    id_client = fields.Int(required=True)
    angel = fields.Str(required=True)
    pole = fields.Str(required=True)
    deadline = fields.Function(serialize=lambda obj: obj.deadline, deserialize=parse_date, required=True)
    attendance_date = fields.Function(serialize=lambda obj: obj.attendance_date, deserialize=parse_date, required=True)

    #TODO: add personalized validations on schema
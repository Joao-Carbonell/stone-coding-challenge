import datetime

from marshmallow import Schema, fields, ValidationError, validates, post_load

from app.config.config import db
from app.models.attendance.attendance_model import Attendance
from app.utils.date_utils import parse_date


class AttendanceCreationSchema(Schema):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    id_attendance = fields.Int(required=True)
    id_client = fields.Int(required=True)
    angel = fields.Str(required=True)
    pole = fields.Str(required=True)
    deadline = fields.Function(serialize=lambda obj: obj.deadline, deserialize=parse_date, required=True)
    attendance_date = fields.Function(serialize=lambda obj: obj.attendance_date, deserialize=parse_date, required=False)

    @post_load
    def make_attendance(self, data, **kwargs):
        return Attendance(id_attendance = data['id_attendance'],
                           id_client = data['id_client'],
                           angel = data['angel'],
                           pole = data['pole'],
                           deadline = data['deadline'],
                           attendance_date = data['attendance_date'])


    #TODO: add personalized validations on schema
    @validates('id_attendance')
    def validate_id_attendance(self, value):
        if value <= 0:
            raise ValidationError("INVALID_ATTENDANCE_ID")

    @validates('id_client')
    def validate_id_client(self, value):
        if value <= 0:
            raise ValidationError("INVALID_CLIENT_ID")

    @validates('deadline')
    def validate_deadline(self, value):
        if not isinstance(value, datetime.datetime):
            raise ValidationError("INVALID_DEADLINE")

    @validates('angel')
    def validate_angel(self, value):
        if len(value) <= 0:
            raise ValidationError("INVALID_ANGEL_NAME")

    @validates('pole')
    def validate_pole(self, value):
        if len(value) <= 0:
            raise ValidationError("INVALID_POLE_NAME")
from app.config.config import db


class FileRecord(db.Model):
    __tablename__ = 'file_records'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String, unique=True, nullable=False)
    processed_at = db.Column(db.DateTime, nullable=False)

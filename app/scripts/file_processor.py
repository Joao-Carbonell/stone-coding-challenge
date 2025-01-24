import hashlib

from app.config.config import db
from app.models.file_record_model import FileRecord


def get_file_hash(file_path):
    """
    Computes the MD5 hash of a given file.

    This function reads the entire content of the file located at the provided
    path, computes the MD5 hash of the file's binary content, and returns the
    resulting hash as a hexadecimal string.

    :param file_path: The path to the file whose MD5 hash is to be computed.
    :type file_path: str
    :return: The MD5 hash of the file's binary content as a hexadecimal string.
    :rtype: str
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def check_file_processed(file_hash):
    """
    Checks whether a file with the specified hash has already been processed.

    This function queries the database to check for the existence of a record
    with a hash matching the provided file_hash. It helps to determine if a file
    has already been processed and stored in the database.

    :param file_hash: The hash of the file to check.
    :type file_hash: str

    :return: True if the file is already processed (exists in the database),
        False otherwise.
    :rtype: bool
    """
    return db.session.query(db.exists().where(FileRecord.hash == file_hash)).scalar()


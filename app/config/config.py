import os

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()

#Configuration class for db
class Config:
    """
    Configuration class for the application.

    Provides configuration settings for the application, such as database URI
    and track modifications options.

    :ivar SQLALCHEMY_TRACK_MODIFICATIONS: Defines whether SQLAlchemy should
        track modifications of objects. Recommended to set to False for better
        performance.
    :type SQLALCHEMY_TRACK_MODIFICATIONS: bool
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

def connect_tcp_socket() -> str:
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]

    if os.getenv("FLASK_DEBUG") == "1":
        host = "127.0.0.1"
        port = os.environ.get("DB_PORT", "5432")
        return str(os.environ.get('SQLALCHEMY_DATABASE_URI'))
    else:

        project_id = os.environ["GCP_PROJECT_ID"]
        instance_connection_name = os.environ["INSTANCE_HOST"]
        return f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{project_id}:{instance_connection_name}"


import os
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

# Create a SQLAlchemy session
session = Session(db)

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
    :ivar SQLALCHEMY_DATABASE_URI: Defines the database connection URI,
        retrieved from the environment variable 'DB_URL'.
    :type SQLALCHEMY_DATABASE_URI: str
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost:5432/kpi-api-database"


    engine = create_engine(SQLALCHEMY_DATABASE_URI)


    Session = sessionmaker(bind=engine)
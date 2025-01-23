import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from app.config.config import Config, jwt
from app.models.client.client import Client
from app.routes import register_routes
from app.config.config import db
from app.scripts.load_data_csv import load_csv_to_db

"""
This __init__ class is responsible for create the app, 
loading configuration from the configuration file, 
registering routes, and initialize the database
"""
#TODO: Must to move the configuration values to the environment file
def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config["API_TITLE"] = os.environ.get('API_TITLE')
    app.config["FLASK_DEBUG"] = os.environ.get('FLASK_DEBUG')
    app.config["API_VERSION"] = os.environ.get('API_VERSION')

    app.config["OPENAPI_VERSION"] = os.environ.get('OPENAPI_VERSION')
    app.config["OPENAPI_URL_PREFIX"] = os.environ.get('OPENAPI_URL_PREFIX')
    app.config["OPENAPI_SWAGGER_UI_PATH"] = os.environ.get('OPENAPI_SWAGGER_UI_PATH')
    app.config["OPENAPI_SWAGGER_UI_URL"] = os.environ.get('OPENAPI_SWAGGER_UI_URL')
    app.config["OPENAPI_REDOC_PATH"] = os.environ.get('OPENAPI_REDOC_PATH')
    app.config["OPENAPI_REDOC_UI_URL"] = os.environ.get('OPENAPI_REDOC_UI_URL')

    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config["JWT_TOKEN_LOCATION"] = os.environ.get('JWT_TOKEN_LOCATION')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'secret_key')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret_key')

    app.config.from_object(Config)

    print("SQLALCHEMY_DATABASE_URI:", str(os.getenv("SQLALCHEMY_DATABASE_URI")))

    db.init_app(app)

    jwt.init_app(app)

    api = Api(app)

    register_routes(api)

    with app.app_context():
        print("dlkas dlaksjd çlaks dçolaksjd çalksjlaç~s jdaçl")
        csv_file_path = 'app/data/bd_desafio.csv'
        load_csv_to_db(csv_file_path)


    return app

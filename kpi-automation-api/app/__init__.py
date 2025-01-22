import os

from flask import Flask
from flask_smorest import Api
from app.config.config import Config
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

    app.config["API_TITLE"] = "KPI API"
    app.config["API_VERSION"] = "v3"
    app.config["OPENAPI_VERSION"] = "3.1.1"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_UI_URL"] = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"

    app.config.from_object(Config)

    db.init_app(app)

    api = Api(app)

    register_routes(api)

    with app.app_context():

        csv_file_path = 'app/data/bd_desafio.csv'
        load_csv_to_db(csv_file_path)

    return app

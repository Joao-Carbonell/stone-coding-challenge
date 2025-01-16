from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config

db = SQLAlchemy()

#Init python app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    #Routes register
    from app.routes import register_routes
    register_routes(app)

    return app

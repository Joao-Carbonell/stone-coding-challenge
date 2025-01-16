from flask import Flask
from .general_routes import general_blueprint
from .attendance_routes import attendance_blueprint

def register_routes(app: Flask):
    app.register_blueprint(general_blueprint)
    app.register_blueprint(attendance_blueprint, url_prefix='/api')
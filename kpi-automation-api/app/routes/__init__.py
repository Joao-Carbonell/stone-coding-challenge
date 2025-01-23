from .analytics_routes import productivity_blueprint
from .auth_routes import auth_blueprint
from .general_routes import general_blueprint
from .attendance_routes import attendance_blueprint

"""
This method is used to register routes as blueprint
"""
def register_routes(api):
    api.register_blueprint(general_blueprint)
    api.register_blueprint(attendance_blueprint, url_prefix="/api/attendances")
    api.register_blueprint(productivity_blueprint, url_prefix="/api/analytics")
    api.register_blueprint(auth_blueprint)
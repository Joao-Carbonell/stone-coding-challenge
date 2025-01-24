from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from app.controllers.authorization_controller import AuthorizationController
from app.models.api_client.api_client import ApiClient

general_blueprint = Blueprint("Home",'general', url_prefix="/", description="API home")

# Routes for API's general endpoints
@general_blueprint.route("/")
class HomeCollection(MethodView):
    """
    Represents the home endpoint of the API

    This class handles GET requests to home route
    """
    @general_blueprint.response(200, description="Home endpoint")
    def get(self):
        """
        Handles GET request to the endpoint

        :return: A JSON response with a message
        """
        return {"message": "Welcome to Pedra Pagamentos!"}

@general_blueprint.response(200, description="/token")
def get_token():
    return AuthorizationController.get_token()

@general_blueprint.route("/home")
class HomeCollection(MethodView):
    """
    Represents the home endpoint of the API

    This class handles GET requests to home route
    """
    @general_blueprint.response(200, description="Home endpoint")
    def get(self):
        """
        Handles GET request to the endpoint

        :return: A JSON response with a message
        """
        return {"message": "Welcome to Pedra Pagamentos!"}



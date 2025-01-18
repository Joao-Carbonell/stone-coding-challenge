from flask import jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort

general_blueprint = Blueprint("Home",'general', url_prefix="/api", description="API Home")


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




from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from app.models.client.client import Client

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
    data = request.json
    if not data or 'client_key' not in data or 'client_secret' not in data:
        return jsonify({'error': 'Chave e segredo são obrigatórios'}), 400

    client = Client.query.filter_by(client_key=data['client_key']).first()
    if not client or not client.verify_secret(data['client_secret']):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    token = create_access_token(identity={'client_key': client.client_key})
    return jsonify({'access_token': token})

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



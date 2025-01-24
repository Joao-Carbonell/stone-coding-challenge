from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from app.controllers.authorization_controller import AuthorizationController

auth_blueprint = Blueprint("Auth",'auth', url_prefix="/authorization", description="Authorization endpoints")

@auth_blueprint.route("/")
class AuthCollection(MethodView):
    """
    Represents the authorization collection endpoint.

    This class implements the logic for the main authorization API collection
    endpoint. It serves as the entry point for interacting with the authorization
    API and provides details of the available operations.

    """
    @auth_blueprint.response(200)
    def get(self):
        return {'message': 'Authorization API'}

# Route to obtain the token to authenticate
@auth_blueprint.route('/token', methods=['POST'])
def get_token():
    """
    Handles the retrieval of an authentication token for the user.

    This endpoint is triggered by a POST request to the `/token` route
    for obtaining a JWT or similar token used for authentication purposes.
    It utilizes the `get_token` method of `AuthorizationController` to
    process and generate the token.

    :raises ValueError: If the token generation parameters are invalid.
    :raises TypeError: If there is a mismatch in expected types during token processing.

    :return: Response object containing the authentication token.
    :rtype: flask.Response
    """
    try:
        return AuthorizationController.get_token()
    except KeyError as e:
        return jsonify({'error': f'Missing key or secret: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'INTERNAL_SERVER_ERROR', 'details': str(e)}), 500
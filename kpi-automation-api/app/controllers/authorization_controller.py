from flask import request

from app.services.authorization_service import AuthorizationService

# Controller for authorization
class AuthorizationController:

    # Method for getting the authorization's token
    @staticmethod
    def get_token():
        """
        Retrieves a token using data extracted from the incoming request.

        The method fetches JSON-formatted data from the request and uses it to obtain a token
        via the `AuthorizationService`. This is a static method, meaning it can be called
        without an instance of the class.

        :raises KeyError: If expected keys are missing in the request's JSON data.
        :param data: The JSON payload containing the necessary information to
                     generate the token using the `AuthorizationService`.
                     Expected structure and keys depend on the implementation
                     of `AuthorizationService.get_token`.
        :type data: dict
        :return: The token obtained from `AuthorizationService` based on the provided data.
        :rtype: Any
        """
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON payload")
        return AuthorizationService.get_token(data)
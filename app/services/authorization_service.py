from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app import ApiClient
from app.repositories.client_repository import ClientRepository

# Service to manipulate api_client data from model and return to controller
class AuthorizationService:

    @staticmethod
    def get_token(data):
        """
        Retrieves an access token for a api_client by validating the provided api_client key and api_client
        secret. The method checks that the api_client key and api_client secret are present in the input
        data and that they correspond to a valid and authorized api_client. If the validation succeeds,
        it generates and returns a new access token tied to the api_client's identity.

        :param data: A dictionary containing api_client credentials, where the key 'client_key'
                     maps to the api_client's unique identifier and the key 'client_secret' maps
                     to the api_client's secret key for verification.
        :type data: dict
        :return: An access token representing the authorized identity of the api_client if credentials
                 are successfully validated.
        :rtype: str
        :raises ValueError: If the input data does not contain both 'client_key' and 'client_secret'.
        :raises PermissionError: If the api_client is not found or the api_client secret does not match
                                 the provided api_client key.
        """
        # Verify if client_key and client_secret are valid
        if 'api_client_key' not in data or 'api_client_secret' not in data:
            raise ValueError("KEY_AND_SECRET_MANDATORY")

        # Retrieve the api_client from the repository and verify the secret key
        client = ClientRepository.get_client_by_key(data['api_client_key'])
        if not client or not client.verify_secret(data['api_client_secret']):
            raise PermissionError("INVALID_CREDENTIALS")

        # Generate and return an access token for the api_client's identity
        token =  create_access_token(identity={'api_client_key': client.api_client_key})

        return jsonify({'token': token})

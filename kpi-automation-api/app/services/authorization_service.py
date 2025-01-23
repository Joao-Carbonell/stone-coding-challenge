from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app import Client
from app.repositories.client_repository import ClientRepository

# Service to manipulate client data from model and return to controller
class AuthorizationService:

    @staticmethod
    def get_token(data):
        """
        Retrieves an access token for a client by validating the provided client key and client
        secret. The method checks that the client key and client secret are present in the input
        data and that they correspond to a valid and authorized client. If the validation succeeds,
        it generates and returns a new access token tied to the client's identity.

        :param data: A dictionary containing client credentials, where the key 'client_key'
                     maps to the client's unique identifier and the key 'client_secret' maps
                     to the client's secret key for verification.
        :type data: dict
        :return: An access token representing the authorized identity of the client if credentials
                 are successfully validated.
        :rtype: str
        :raises ValueError: If the input data does not contain both 'client_key' and 'client_secret'.
        :raises PermissionError: If the client is not found or the client secret does not match
                                 the provided client key.
        """
        # Verify if client_key and client_secret are valid
        if 'client_key' not in data or 'client_secret' not in data:
            raise ValueError("KEY_AND_SECRET_MANDATORY")

        # Retrieve the client from the repository and verify the secret key
        client = ClientRepository.get_client_by_key(data['client_key'])
        if not client or not client.verify_secret(data['client_secret']):
            raise PermissionError("INVALID_CREDENTIALS")

        # Generate and return an access token for the client's identity
        token =  create_access_token(identity={'client_key': client.client_key})

        return jsonify({'token': token})

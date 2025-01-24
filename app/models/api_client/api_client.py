import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.config import db


# This model is used to represent the API's api_client
class ApiClient(db.Model):
    """
    Represents an API client object, used for managing API client credentials and their
    verification.

    This class interacts with a database table named 'api_clients' and provides necessary
    functionality to hash and verify API client secrets, ensuring secure storage and
    authentication. Its main purpose is to serve as a model object for storing important
    details like `client_key` and `client_secret` as well as utilities for secure handling
    of credentials.

    Attributes:
        id: A unique identifier for each API client in the table.
        api_client_key: A unique string key for the API client.
        client_secret: A hashed text representing the secret key for the API client.

    Methods:
        hash_secret(secret):
            Static method to securely hash an API client's secret key.

        verify_secret(secret):
            Instance method to verify a provided API client secret by comparing it with
            the stored hashed secret.

    """
    __tablename__ = 'api_clients'

    id = db.Column(db.Integer, primary_key=True)
    api_client_key = db.Column(db.String(64), unique=True, nullable=False)
    api_client_secret = db.Column(db.Text, nullable=False)

    # Method fo generate api_client's secret
    @staticmethod
    def hash_secret(secret):
        return generate_password_hash(secret, method='pbkdf2:sha256', salt_length=16)

    # Method to verify api_client's secret comparing against the sent secret
    def verify_secret(self, secret):
        return check_password_hash(self.api_client_secret, secret)
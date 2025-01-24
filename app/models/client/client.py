import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.config import db


# This model is used to represent the API's client
class Client(db.Model):
    """
    Represents a Client entity for use in the database.

    This class is an ORM model defining the structure of a "clients" table in the database,
    along with utility methods for securely hashing and verifying secrets. It includes
    attributes representing the unique client key and the hashed client secret. Instances
    of this class can be used for purposes related to client authentication and security.

    :ivar id: Unique identifier for the client record.
    :type id: int
    :ivar client_key: Unique key associated with the client.
    :type client_key: str
    :ivar client_secret: Hashed secret associated with the client.
    :type client_secret: str
    """
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    client_key = db.Column(db.String(64), unique=True, nullable=False)
    client_secret = db.Column(db.Text, nullable=False)

    # Method fo generate client's secret
    @staticmethod
    def hash_secret(secret):
        return generate_password_hash(secret, method='pbkdf2:sha256', salt_length=16)

    # Method to verify client's secret comparing against the sent secret
    def verify_secret(self, secret):
        return check_password_hash(self.client_secret, secret)
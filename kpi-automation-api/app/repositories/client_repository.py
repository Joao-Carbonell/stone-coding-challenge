from app import Client

# Repository class to handler on client db table
class ClientRepository:

    @staticmethod
    def get_client_by_key(client_key):
        """
        Fetches a client from the database using the provided client key.

        This method queries the database for a client matching the given
        client key. It utilizes the `filter_by` method to locate the first
        entry corresponding to the provided key. If no matching client is
        found, the method returns `None`.

        :param client_key: The unique key identifying the client in the database.
        :type client_key: str

        :return: The client object corresponding to the provided key, or
            `None` if no matching client is found.
        :rtype: Client or None
        """
        # Uses the client_key to locate the first entry corresponding
        if not client_key:
            raise ValueError("Client key cannot be empty")

        client = Client.query.filter_by(client_key=client_key).first()
        if not client:
            return None
        return client
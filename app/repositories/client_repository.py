from app import ApiClient

# Repository class to handler on api_client db table
class ClientRepository:

    @staticmethod
    def get_client_by_key(api_client_key):
        """
        Fetches a api_client from the database using the provided api_client key.

        This method queries the database for a api_client matching the given
        api_client key. It utilizes the `filter_by` method to locate the first
        entry corresponding to the provided key. If no matching api_client is
        found, the method returns `None`.

        :param api_client_key: The unique key identifying the api_client in the database.
        :type api_client_key: str

        :return: The api_client object corresponding to the provided key, or
            `None` if no matching api_client is found.
        :rtype: ApiClient or None
        """
        # Uses the client_key to locate the first entry corresponding
        if not api_client_key:
            raise ValueError("API client key cannot be empty")

        client = ApiClient.query.filter_by(api_client_key=api_client_key).first()
        if not client:
            return None
        return client
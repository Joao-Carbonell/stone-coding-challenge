from app import db, create_app, ApiClient


def create_db():
    """
    Creates all the database tables defined in the application's models.

    This function initializes a Flask application by invoking the `create_app`
    function. It then sets up the application context using a `with` block,
    allowing operations that require the context (such as database table creation)
    to be performed. Inside the block, it imports the `Attendance` model from the
    application's models and creates all tables in the database defined by the
    SQLAlchemy models.

    :raises OperationalError: If there's an error during database creation.
    :raises ImportError: If models couldn't be imported during execution.
    :return: None
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        with app.app_context():
            db.create_all()
            if not ApiClient.query.first():
                secret = 'secret_key'
                client = ApiClient(api_client_key='my_client', api_client_secret=ApiClient.hash_secret(secret))
                db.session.add(client)
                db.session.commit()
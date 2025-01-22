from app import create_app
from app.config.create_db import create_db

"""
Mainly script to initialize the flask server
 - Create a new database if it doesn't exist'
 - Run the python run.py to start the server
 - When running in docker container dockerfile will use gunicorn
"""
app = create_app()
# Create db with app context
with app.app_context():
    create_db()
#Init flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

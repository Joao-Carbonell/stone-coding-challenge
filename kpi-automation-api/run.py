import os

import uvicorn
from dotenv import load_dotenv

from app import create_app
from app.config.create_db import create_db

"""
Main script to initialize the flask server
 - Create a new database if it doesn't exist'
 - Run the python run.py to start the server
 - When running in docker container dockerfile will use gunicorn
"""

# Create a flask
app = create_app()
# Create db with app context
with app.app_context():
    create_db()
# Run flask server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("run:app", host="0.0.0.0", port=port)
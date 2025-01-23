# Python image
FROM python:3.10-slim

# Defining directory
WORKDIR /app

# Coping the requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Coping the requirements
COPY . /app/

# Exposing 8000 port
EXPOSE 8000

# Run flask
CMD ["python", "run.py"]
# Python image
FROM python:3.9-slim

# Defining directory
WORKDIR /app

# Coping the requirements.txt
COPY requirements.txt /app/

# Instalar dependências
RUN pip install -r requirements.txt

# Coping the requirements
COPY . /app/

# Exposing 8000 port
EXPOSE 8000

# Run flask
CMD ["python", "run.py"]

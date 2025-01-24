# Python image
FROM python:3.10-slim


ARG ENV=production


ENV APP_ENV=$ENV

# Defining directory
WORKDIR /app

# Coping the requirements.txt
COPY requirements.txt /app/

COPY . /app/
RUN if [ "$APP_ENV" = "development" ]; then \
      echo "Copying .env into container..."; \
      cp /app/.env /app/.env; \
    else \
      echo "Production environment, ignoring .env..."; \
    fi

# Install dependencies
RUN pip install -r requirements.txt

# Coping the requirements
COPY . /app/

# Exposing 8000 port
EXPOSE 8000

# Run flask
CMD ["python", "run.py"]
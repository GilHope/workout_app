### Build stage ###
FROM python:3.10-slim as build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf for PDF generation
RUN apt-get update && apt-get install -y wkhtmltopdf 

COPY workout_app/ /app/

### Prod stage ###
FROM python:3.10-slim

WORKDIR /app

COPY --from=build /app /app

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ARG ENVIRONMENT=production

# Default command for Gunicorn in production mode
CMD if [ "$ENVIRONMENT" = "development" ]; then flask run --host=0.0.0.0; else gunicorn --bind 0.0.0.0:5000 app:app; fi

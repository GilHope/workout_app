FROM python:3.10-slim

WORKDIR /app

# Install wkhtmltopdf for PDF generation
RUN apt-get update && apt-get install -y wkhtmltopdf && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0"]
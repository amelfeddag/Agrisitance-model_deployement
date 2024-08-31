FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render uses the PORT environment variable
ENV PORT=10000

# Use gunicorn as the production server
CMD gunicorn --bind 0.0.0.0:$PORT server:app

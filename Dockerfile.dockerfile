FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000

CMD gunicorn --bind 0.0.0.0:$PORT --log-level debug --timeout 1500  server:app

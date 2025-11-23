FROM python:3.11-slim

# Dépendances système minimales pour Androguard
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libxml2-dev libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/uploads

ENV PORT=8002
EXPOSE 8002

CMD ["gunicorn", "-b", "0.0.0.0:8002", "app:app", "--workers", "2", "--timeout", "120"]
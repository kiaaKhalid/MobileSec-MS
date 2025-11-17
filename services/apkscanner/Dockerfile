FROM python:3.11-slim

# dépendances système nécessaires pour python-magic et androguard
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libmagic1 libxml2 libxslt1.1 python3-dev default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN mkdir -p /app/uploads

ENV PORT=8001
EXPOSE 8001

CMD ["gunicorn", "-b", "0.0.0.0:8001", "app:app", "--workers", "1"]


FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8006

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8006", "app:app"]

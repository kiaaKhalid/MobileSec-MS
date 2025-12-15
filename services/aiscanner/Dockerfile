# Utiliser une image Python officielle légère mais compatible (3.9 ou 3.10 conseillé pour TF)
FROM python:3.9-slim

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires pour TensorFlow/Androguard
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copie des requirements et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et du modèle
COPY . .

# Exposition du port
EXPOSE 5005
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5005"]

FROM python:3.13

# Definition du workspace
WORKDIR /app

# Mise à jour de pip
RUN pip install --no-cache-dir --upgrade pip

# Installation des dépendances (copiées séparément pour optimiser le cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port utilisé par Flask
EXPOSE 5000

# Script d'entrée pour initialiser la BD puis démarrer l'app
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 --timeout 120 monApp.app:app"]
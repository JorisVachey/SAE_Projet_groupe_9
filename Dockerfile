# Utilisation d'une image Python légère
FROM python:3.11-slim

# Définition du répertoire de travail
WORKDIR /monApp

# Installation des dépendances (copiées séparément pour optimiser le cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port utilisé par Flask
EXPOSE 5000

# Commande de lancement via Gunicorn
# -w 4 : nombre de workers
# -b 0.0.0.0:5000 : bind sur toutes les interfaces du conteneur
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
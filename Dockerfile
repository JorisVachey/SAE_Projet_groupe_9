FROM python:3.12

# Définition du workspace
WORKDIR /app

# Mise à jour de pip
RUN pip install --no-cache-dir --upgrade pip

# Installation des dépendances (copiées séparément pour optimiser le cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .
RUN chmod +x initdb.sh

# Exposition du port utilisé par Flask
EXPOSE 5000

# Utilisation du script comme point d'entrée
CMD ["flask","run","--host=0.0.0.0"]

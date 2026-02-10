#!/bin/sh
set -e

echo "⏳ Attente de MariaDB..."

# Variables d'environnement
HOST=${DB_HOST:-db}
USER=${DB_USER:-user}
PASSWORD=${DB_PASSWORD:-password}
DATABASE=${DB_NAME:-db}
PORT=${DB_PORT:-3306}

# Attente de la base via Python + pymysql
while true; do
    python - <<END
import pymysql, os
try:
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "$HOST"),
        user=os.getenv("DB_USER", "$USER"),
        password=os.getenv("DB_PASSWORD", "$PASSWORD"),
        database=os.getenv("DB_NAME", "$DATABASE"),
        port=int(os.getenv("DB_PORT", "$PORT")),
        connect_timeout=2
    )
    conn.close()
except Exception as e:
    raise SystemExit(1)
END
    if [ $? -eq 0 ]; then
        echo "✅ MariaDB est prête"
        break
    else
        echo "⏳ MariaDB pas encore prête, retry..."
        sleep 2
    fi
done

# Création des tables si elles n'existent pas
echo "⚙️  Création des tables si nécessaire..."
python - <<END
from monApp.app import db, app
with app.app_context():
    db.create_all()
END
echo "✅ Tables prêtes"

# Lancer Gunicorn
echo "🚀 Démarrage de l'application Flask..."
exec gunicorn --bind 0.0.0.0:5000 --timeout 120 monApp.app:app

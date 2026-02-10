#!/usr/bin/env python
"""Script pour initialiser la base de données"""

import os
import time
from monApp.app import app, db

def wait_for_db():
    """Attendre que la base de données soit disponible"""
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        try:
            with app.app_context():
                db.engine.connect()
                print("✓ Connexion à la base de données réussie")
                return True
        except Exception as e:
            attempt += 1
            print(f"⏳ Tentative {attempt}/{max_attempts}: Attente de la base de données...")
            time.sleep(2)

    print("✗ Impossible de se connecter à la base de données après 30 tentatives")
    return False

def init_db():
    """Initialiser la base de données"""
    with app.app_context():
        print("🔧 Création des tables...")
        db.create_all()
        print("✓ Tables créées avec succès")

if __name__ == "__main__":
    if wait_for_db():
        init_db()
        print("✓ Initialisation complète!")
    else:
        exit(1)

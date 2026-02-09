import pytest
import os
from monApp.app import app, db
from monApp.models import User, Plat, Type_plat, Reservation
from hashlib import sha256

@pytest.fixture
def testapp():
    # Configuration de la BDD de test (Fichier temporaire pour stabilité)
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
    
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_secret_key"
    })

    # Nettoyage initial
    if os.path.exists(db_path):
        os.remove(db_path)

    with app.app_context():
        db.create_all()
        
        # 1. Type de Plat
        entree = Type_plat(idTp=1, nomTp="Entrée", descriptionTp="Froid", cheminImg="e.jpg")
        db.session.add(entree)
        
        # 2. Plat
        plat = Plat(
            nomP="Salade César", 
            idTp=1, 
            prixP=12.50, 
            stock=20, 
            cheminImg="salade.jpg", 
            descriptionP="Laitue"
        )
        # On force stockInit manuellement (car pas de trigger en SQLite)
        plat.stockInit = 20 
        db.session.add(plat)
        
        # 3. Utilisateurs
        m = sha256()
        m.update("password123".encode("utf-8"))
        pwd = m.hexdigest()

        # --- CORRECTION ICI : On retire idUser du constructeur ---
        
        # Client Standard
        user = User(
            numtelUser="0600000001", 
            pseudonyme="client", 
            mdp=pwd, 
            est_admin=False
        )
        user.idUser = 1
        
        # Admin
        admin = User(
            numtelUser="0600000002", 
            pseudonyme="admin", 
            mdp=pwd, 
            est_admin=True
        )
        admin.idUser = 2
        
        db.session.add_all([user, admin])
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

    # Nettoyage final
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def client(testapp):
    return testapp.test_client()

@pytest.fixture
def session(testapp):
    with testapp.app_context():
        yield db.session
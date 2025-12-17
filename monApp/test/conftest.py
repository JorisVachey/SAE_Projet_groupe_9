import pytest
from monApp.app import app, db
from monApp.models import User, Plat, Type_plat, Formule
from hashlib import sha256

@pytest.fixture
def testapp():
    # Configuration de l'application pour les tests
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        
        # 1. Création d'un type de plat
        entree = Type_plat(idTp=1, nomTp="Entrée", descriptionTp="Plats froids", cheminImg="entree.jpg")
        db.session.add(entree)
        
        # 2. Création d'un plat de test
        plat = Plat(nomP="Salade César", idTp=1, prixP=12.50, stock=20, cheminImg="salade.jpg", descriptionP="Laitue, poulet, parmesan")
        db.session.add(plat)
        
        # 3. Création d'un utilisateur de test (admin)
        m = sha256()
        m.update("password123".encode())
        user = User(
            numtelUser="0102030405",
            pseudonyme="testuser",
            mdp=m.hexdigest(),
            est_admin=True
        )
        db.session.add(user)
        db.session.commit()
        
        yield app
        
        # Nettoyage après les tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(testapp):
    """Un client HTTP pour les tests fonctionnels."""
    return testapp.test_client()

@pytest.fixture
def session(testapp):
    """Une session de base de données pour les tests unitaires."""
    with testapp.app_context():
        yield db.session
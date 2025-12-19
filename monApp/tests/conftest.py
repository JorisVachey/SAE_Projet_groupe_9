import pytest
from monApp.app import app, db
from monApp.models import User, Plat, Type_plat
from hashlib import sha256

@pytest.fixture
def testapp():
    # Configuration de l'application pour les tests (SQLite en mémoire)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        # 1. Création d'un type de plat de test
        entree = Type_plat(
            idTp=1, 
            nomTp="Entrée", 
            descriptionTp="Plats froids", 
            cheminImg="entree.jpg"
        )
        db.session.add(entree)
        # 2. Création d'un plat de test
        plat = Plat(
            nomP="Salade César", 
            idTp=1, 
            prixP=12.50, 
            stock=20, 
            cheminImg="salade.jpg", 
            descriptionP="Laitue, poulet, parmesan"
        )
        db.session.add(plat)
        # 3. Création d'un utilisateur de test (admin)
        m = sha256()
        m.update("password123".encode())
        user = User(
            numtelUser="0102030405",
            pseudonyme="testuser",
            mdp=m.hexdigest(),
            est_admin=False
        )
        admin = User(numtelUser="0600000000", pseudonyme="admin", mdp="hash...", est_admin=True)
        db.session.add_all([user,admin])
        
        db.session.commit()
        
        yield app
        
        # Nettoyage après les tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(testapp):
    """Fixture pour simuler des requêtes HTTP sur les routes."""
    return testapp.test_client()

@pytest.fixture
def session(testapp):
    """Fixture pour interagir directement avec l'ORM dans les tests unitaires."""
    with testapp.app_context():
        yield db.session
import io
import pytest
import json
from monApp.models import *



def force_login_user(client, user_id=1):
    """
    Force la connexion d'un utilisateur en manipulant la session Flask.
    Contourne le formulaire de login et le hachage de mot de passe.
    """
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)
        sess['_fresh'] = True

def force_login(client, user_id):
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)
        sess['_fresh'] = True

def force_login_admin(client):
    """Force la connexion de l'admin (ID 2 dans ton conftest)."""
    force_login_user(client, user_id=2)

def login_standard(client):
    """Connecte le client via la route officielle."""
    return client.post('/connection/', data={
        'numtelUser': '0600000000',
        'mdp': 'password123'
    }, follow_redirects=True)

def login_admin(client):
    """Connecte l'admin via la route officielle."""
    return client.post('/connection/', data={
        'numtelUser': '0600000000',
        'mdp': 'password123'
    }, follow_redirects=True)
def test_index(client):
    """Vérifie que la page d'accueil charge."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"TypeDePlats" in response.data or b"Entr\xc3\xa9e" in response.data

def test_menu(client):
    """Vérifie l'affichage du menu."""
    response = client.get('/menu/')
    assert response.status_code == 200
    assert b"Salade C\xc3\xa9sar" in response.data



def test_creation_automatique_panier(client, session):
    """Vérifie qu'accéder au panier en crée un vide s'il n'existe pas."""
    force_login_user(client)
    resa_avant = Reservation.query.filter_by(idUser=1, statut="EN ATTENTE").first()
    assert resa_avant is None
    response = client.get('/panier/')
    assert response.status_code == 200
    resa_apres = Reservation.query.filter_by(idUser=1, statut="EN ATTENTE").first()
    assert resa_apres is not None




def test_admin_validation_commande_et_stock(client, session):
    """Test admin valide commande et décrémente stock."""
    force_login(client, user_id=1)
    client.post('/ajouter_plat/1')
    client.post('/panier/valider')
    force_login(client, user_id=2)
    resa = Reservation.query.filter_by(statut="CONFIRMÉE").first()
    url = f'/admin/preparer_panier/{resa.idR}/valider'
    response = client.post(url, follow_redirects=True)
    assert response.status_code == 200
    session.refresh(resa)
    assert resa.statut == "VENIR CHERCHER"
    plat = session.get(Plat, 1)
    assert plat.stock == 19


def test_update_checkbox_sur_place(client, session):
    """Teste la route AJAX pour changer 'sur place'."""
    force_login_user(client)
    client.get('/panier/')
    resa = Reservation.query.filter_by(idUser=1).first()
    payload = {'idR': resa.idR, 'sur_place': True}
    response = client.post('/update_checkbox', 
                           data=json.dumps(payload), 
                           content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['sur_place'] is True


def test_admin_acces_protege(client):
    """Un user normal ne doit pas accéder à l'admin."""
    force_login_user(client)
    response = client.get('/admin/', follow_redirects=True)
    assert response.request.path == "/" or response.request.path == "/index/"

def test_admin_creation_plat(client, session):
    """L'admin crée un plat (avec upload image simulé)."""
    force_login_admin(client)
    data = {
        'nomP': 'Nouveau Plat',
        'idTp': 1,
        'prixP': 15.0,
        'stock': 10,
        'desc': 'Description',
        'image': (io.BytesIO(b"fake image content"), 'test.jpg')
    }
    response = client.post('/admin/gestion_plats/', 
                           data=data, 
                           content_type='multipart/form-data')
    assert response.status_code == 200
    json_resp = response.get_json()
    assert json_resp['success'] is True
    plat = Plat.query.filter_by(nomP="Nouveau Plat").first()
    assert plat is not None
    assert plat.stock == 10


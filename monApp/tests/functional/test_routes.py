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

def test_admin_creation_plat(client):
    """L'admin crée un plat (avec upload image simulé)."""
    force_login_admin(client)
    data = {
        'nomP': 'Nouveau Plat',
        'idTp': 1,
        'prixP': 15.0,
        'stockInit': 10,
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

def test_admin_suppression_plat(client, session):
    """L'admin supprime un plat."""
    force_login_admin(client)
    plat = Plat(nomP="Plat A Supprimer", idTp=1, prixP=10.0,  stockInit=5, cheminImg="...", descriptionP="...")
    session.add(plat)
    session.commit()
    response = client.delete(f'/supprimer-plat/{plat.nomP}')
    assert response.status_code == 200
    assert response.get_json()['success'] is True
    assert Plat.query.filter_by(nomP="Plat A Supprimer").first() is None

def test_admin_création_formule(client, session):
    """L'admin crée une formule (nécessite un plat existant)."""
    force_login_admin(client)
    plat = Plat(nomP="Plat Test Formule", idTp=1, prixP=10.0,  stockInit=10, cheminImg="", descriptionP="Desc")
    session.add(plat)
    session.commit()

    data = {
        'nomF': 'Nouvelle Formule',
        'prixF': 20.0,
        'plats': [plat.idP], 
        'quantite_' + str(plat.idP): 1,
        'image': (io.BytesIO(b"fake image content"), 'test.jpg')
    }
    
    response = client.post('/admin/gestion_formules/', 
                           data=data, 
                           content_type='multipart/form-data')
    
    assert response.status_code == 200
    json_resp = response.get_json()
    assert json_resp['success'] is True
    
    form = Formule.query.filter_by(nomF="Nouvelle Formule").first()
    assert form is not None
    assert float(form.prixF) == 20.0
    assert len(form.plats) == 1

def test_admin_suppression_formule(client):
    """L'admin supprime une formule."""
    force_login_admin(client)
    form = Formule.query.filter_by(nomF="Nouvelle Formule").first()
    response = client.delete(f'/admin/supprimer-formule/{form.idF}')
    assert response.status_code == 200
    form_deleted = Formule.query.get(form.idF)
    assert form_deleted is None

def test_admin_modification_plat(client,session):
    """L'admin modifie un plat."""
    force_login_admin(client)
    plat = Plat(nomP="Plat Modif Prix", idTp=1, prixP=10.0, stockInit=5, cheminImg="...", descriptionP="...")
    session.add(plat)
    session.commit()
    data = {
        'idP': plat.idP,
        'prixP': 15.0
    }
    response = client.post('/admin/modifier_prix_plat', json=data)
    assert response.status_code == 200
    assert response.get_json()['success'] is True
    session.refresh(plat)
    assert float(plat.prixP) == 15.0

def test_admin_modification_formule(client,session):
    """L'admin modifie une formule."""
    force_login_admin(client)
    form = Formule(idF=200, nomF="Formule Modif", prixF=15.0, cheminImg="img.png")
    session.add(form)
    session.commit()
    data = {
        'idF': form.idF,
        'prixF': 18.0
    }
    response = client.post('/admin/modifier_prix_formule', json=data)
    assert response.status_code == 200
    assert response.get_json()['success'] is True
    session.refresh(form)
    assert float(form.prixF) == 18.0



def test_contact(client):
    response = client.get("/contact/")
    assert response.status_code == 200

def test_nouveauter(client):
    response = client.get("/nouveautes/")
    assert response.status_code == 200

def test_connection(client):
    response = client.get("/connection/")
    assert response.status_code == 200

def test_déco(client):
    force_login_user(client)
    response = client.get("/deconnection/")
    assert response.status_code == 302  # redirection


def test_inscription(client):
    response = client.get("/inscription/")
    assert response.status_code == 200

def test_chartre(client):
    response = client.get("/chartre/")
    assert response.status_code == 200

def test_mesreservation(client):
    force_login_user(client)
    response = client.get("/mesreservation/")
    assert response.status_code == 200

def test_gestionformule(client):
    force_login_admin(client)
    response = client.get("/admin/gestion_formules/")
    assert response.status_code == 200

def test_gestionformule(client):
    force_login_admin(client)
    response = client.get("/admin/gestion_cli/")
    assert response.status_code == 200

def test_gestionformule(client):
    force_login_admin(client)
    response = client.get("/admin/voir_comm/")
    assert response.status_code == 200

def test_gestionformule(client):
    force_login_admin(client)
    response = client.get("/admin/gestion_compte/")
    assert response.status_code == 200
    
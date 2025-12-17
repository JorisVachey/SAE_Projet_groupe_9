import pytest
from monApp.models import User, Plat, Reservation, ContenirP, Type_plat, db

# --- Utilitaire de connexion ---
def login(client, user_obj):
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_obj.idUser)
        sess['_fresh'] = True

# --- 1. Pages de base ---
def test_navigation_basique(client):
    """Vérifie que les pages principales répondent 200."""
    routes = ['/', '/propos', '/menu/', '/nouveautes/', '/connection/', '/inscription/']
    for route in routes:
        assert client.get(route).status_code == 200

# --- 2. Gestion du Panier (Client) ---
def test_panier_workflow(client, testapp):
    with testapp.app_context():
        user = User.query.filter_by(est_admin=False).first()
        plat = Plat.query.first()
        login(client, user)

        # Ajout
        client.post(f'/ajouter_plat/{plat.idP}', follow_redirects=True)
        
        # Validation : On vérifie si on est redirigé (302) ou si le statut change en BD
        response = client.post('/panier/valider', follow_redirects=True)
        assert response.status_code == 200
        
        resa = Reservation.query.filter_by(idUser=user.idUser).first()
        assert resa is not None
        assert resa.statut in ["CONFIRMÉE", "PAYÉE"]

def test_annuler_panier(client, testapp):
    """Vérifie que le panier est bien supprimé de la BD après annulation."""
    with testapp.app_context():
        user = User.query.filter_by(est_admin=False).first()
        login(client, user)

        # 1. Créer un panier
        client.post('/ajouter_plat/1', follow_redirects=True)
        assert Reservation.query.filter_by(idUser=user.idUser, statut="EN ATTENTE").first() is not None

        # 2. Annuler le panier
        response = client.post('/panier/annuler', follow_redirects=True)
        assert response.status_code == 200

        # 3. Vérification robuste en base de données
        panier = Reservation.query.filter_by(idUser=user.idUser, statut="EN ATTENTE").first()
        assert panier is None

# --- 3. Administration ---
def test_admin_gestion_clients(client, testapp):
    with testapp.app_context():
        admin = User.query.filter_by(est_admin=True).first()
        client_simple = User.query.filter_by(est_admin=False).first()
        
        if not admin or not client_simple:
            pytest.fail("Manque admin ou client dans la fixture.")

        login(client, admin)

        # Bannir
        client.get(f'/admin/bannir-cli/{client_simple.idUser}', follow_redirects=True)
        assert User.query.get(client_simple.idUser).est_banni is True
        
        # Débannir
        client.get(f'/admin/debannir-cli/{client_simple.idUser}', follow_redirects=True)
        assert User.query.get(client_simple.idUser).est_banni is False

def test_admin_traiter_commande(client, testapp):
    """Teste la validation d'une commande (Correction du TypeError sur_place)."""
    with testapp.app_context():
        admin = User.query.filter_by(est_admin=True).first()
        plat = Plat.query.first()
        login(client, admin)

        # Création manuelle d'une résa avec tous les arguments requis
        # Ton modèle demande : idUser, dateR, nb_couverts, sur_place, statut
        from datetime import datetime
        res = Reservation(
            idUser=admin.idUser, 
            dateR=datetime.now(), 
            nb_couverts=2, 
            sur_place=False, 
            statut="CONFIRMÉE"
        )
        db.session.add(res)
        db.session.commit()
        
        # Ajouter un plat à cette résa
        item = ContenirP(idR=res.idR, idP=plat.idP, quantiteP=1)
        db.session.add(item)
        db.session.commit()

        stock_avant = plat.stock
        
        # Admin valide
        client.post(f'/admin/preparer_panier/{res.idR}/valider', follow_redirects=True)
        
        # Vérification stock et statut
        assert Plat.query.get(plat.idP).stock == stock_avant - 1
        assert Reservation.query.get(res.idR).statut == "VENIR CHERCHER"

# --- 4. Sécurité ---
def test_acces_admin_interdit_au_client(client, testapp):
    with testapp.app_context():
        user = User.query.filter_by(est_admin=False).first()
        login(client, user)
        
        # Tentative d'accès à la gestion
        response = client.get('/admin/gestion_plats/', follow_redirects=True)
        # Redirection vers index car non admin
        assert response.request.path in ['/', '/index/']

def test_modifier_prix_plat_json(client, testapp):
    with testapp.app_context():
        admin = User.query.filter_by(est_admin=True).first()
        plat = Plat.query.first()
        login(client, admin)

        payload = {"idP": plat.idP, "prixP": 20.00}
        response = client.post('/admin/modifier_prix_plat', json=payload)
        assert response.json['success'] is True
        assert Plat.query.get(plat.idP).prixP == 20.00
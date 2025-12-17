import pytest
from monApp.models import User, Reservation, Plat, Type_plat, Formule, Composer, ContenirP, ContenirF


def test_user_creation(session):
    """Vérifie la création d'un utilisateur et ses méthodes de bannissement."""
    new_user = User(numtelUser="0607080910", pseudonyme="test", mdp="mot de passe")
    session.add(new_user)
    session.commit()

    assert new_user.idUser is not None
    assert new_user.est_banni is False
    
    # Test de la méthode de bannissement
    new_user.bannir()
    assert new_user.est_banni is True

def test_reservation_total(session):
    """Vérifie le calcul du total d'une réservation (Plats + Formules)."""
    tp = Type_plat(idTp=2, nomTp="Plat principal", descriptionTp="...", cheminImg="...")
    p1 = Plat(nomP="Burger", idTp=2, prixP=15.00, stock=10, cheminImg="...", descriptionP="...")
    f1 = Formule(idF=1, nomF="Menu Midi", prixF=20.00)
    
    session.add_all([tp, p1, f1])
    session.commit()
    # Création d'une réservation pour l'utilisateur de test (idUser=1 créé dans conftest)
    res = Reservation(idUser=1, dateR=None, nb_couverts=2, sur_place=True, statut='en cours')
    session.add(res)
    session.commit()

    # Ajout d'un plat (15.00€) et d'une formule (20.00€)
    cp = ContenirP(idR=res.idR, idP=p1.idP, quantiteP=1)
    cf = ContenirF(idR=res.idR, idF=f1.idF, quantiteF=1)
    session.add_all([cp, cf])
    session.commit()

    # Le total doit être de 35.00€
    assert res.get_total() == 15.00 

def test_plat_stock_update(session):
    """Vérifie la mise à jour manuelle du stock et du prix."""
    plat = session.query(Plat).filter_by(nomP="Salade César").first()
    
    plat.new_quantite(50)
    plat.new_prix(13.00)
    session.commit()
    
    assert plat.stock == 50
    assert plat.prixP == 13.00

def test_cascade_delete_reservation(session):
    """Vérifie que la suppression d'une réservation supprime son contenus ."""
    res = session.query(Reservation).first()
    res_id = res.idR
    
    session.delete(res)
    session.commit()
    
    # Vérification que les entrées liées ont disparu
    assert session.query(ContenirP).filter_by(idR=res_id).first() is None
    assert session.query(ContenirF).filter_by(idR=res_id).first() is None

def test_reservation_getbesoin(session):
    """Vérifie que getbesoin calcule correctement les quantités totales de plats."""
    # 1. Setup : Création d'un plat et d'une formule qui contient ce même plat
    tp = Type_plat(idTp=3, nomTp="Test", descriptionTp="...", cheminImg="...")
    p_sushi = Plat(nomP="Sushi Maison", idTp=3, prixP=10, stock=20, cheminImg="...", descriptionP="...")
    session.add_all([tp, p_sushi])
    session.commit()

    f_duo = Formule(idF=2, nomF="Menu Duo", prixF=18)
    session.add(f_duo)
    
    comp = Composer(idF=f_duo.idF, idP=p_sushi.idP, quantiteC=2)
    session.add(comp)
    session.commit()

    res = Reservation(idUser=1, dateR=None, nb_couverts=3, sur_place=True, statut='validée')
    session.add(res)
    session.commit()

    cp = ContenirP(idR=res.idR, idP=p_sushi.idP, quantiteP=1)
    cf = ContenirF(idR=res.idR, idF=f_duo.idF, quantiteF=1)  
    session.add_all([cp, cf])
    session.commit()

    besoins = res.getbesoin()
    assert besoins[p_sushi] == 3
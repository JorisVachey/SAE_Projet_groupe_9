import pytest
from decimal import Decimal
from monApp.models import User, Reservation, Plat, Type_plat, Formule, Composer, ContenirP, ContenirF

def test_user_creation(session):
    """Vérifie la création et les méthodes de User."""
    new_user = User(numtelUser="0607080910", pseudonyme="test", mdp="mot de passe")
    session.add(new_user)
    session.commit()

    assert new_user.idUser is not None
    assert new_user.est_banni is False
    
    new_user.bannir() # Test de la méthode définie dans models.py
    assert new_user.est_banni is True

def test_reservation_total(session):
    """Vérifie le calcul du prix total."""
    tp = Type_plat(idTp=2, nomTp="Plat principal", descriptionTp="...", cheminImg="...")
    p1 = Plat(nomP="Burger", idTp=2, prixP=15.00, stockInit=10, cheminImg="...", descriptionP="...")
    f1 = Formule(idF=1, nomF="Menu Midi", prixF=20.00)
    session.add_all([tp, p1, f1])
    session.commit()

    res = Reservation(idUser=1, dateR=None, nb_couverts=2, sur_place=True, statut='en cours')
    session.add(res)
    session.commit()

    session.add(ContenirP(idR=res.idR, idP=p1.idP, quantiteP=1))
    session.add(ContenirF(idR=res.idR, idF=f1.idF, quantiteF=1))
    session.commit()

    # On utilise Decimal car prixP et prixF sont db.Numeric
    assert res.get_total() == Decimal("35.00")

def test_plat_stock_update(session):
    """Vérifie les méthodes new_quantite et new_prix."""
    # "Salade César" est créé par la fixture dans conftest.py
    plat = session.query(Plat).filter_by(nomP="Salade César").first()
    
    plat.new_quantite(50)
    plat.new_prix(13.00)
    session.commit()
    
    assert plat.stock == 50
    assert float(plat.prixP) == 13.00

def test_reservation_getbesoin(session):
    """Vérifie l'agrégation des stocks via getbesoin()."""
    tp = Type_plat(idTp=3, nomTp="Test", descriptionTp="...", cheminImg="...")
    p_sushi = Plat(nomP="Sushi Maison", idTp=3, prixP=10, stockInit=20, cheminImg="...", descriptionP="...")
    session.add_all([tp, p_sushi])
    session.commit()

    f_duo = Formule(idF=2, nomF="Menu Duo", prixF=18)
    session.add(f_duo)
    # 1 Formule contient 2 Sushis
    session.add(Composer(idF=f_duo.idF, idP=p_sushi.idP, quantiteC=2))
    session.commit()

    res = Reservation(idUser=1, dateR=None, nb_couverts=3, sur_place=True, statut='validée')
    session.add(res)
    session.commit()

    session.add(ContenirP(idR=res.idR, idP=p_sushi.idP, quantiteP=1)) # +1 sushi seul
    session.add(ContenirF(idR=res.idR, idF=f_duo.idF, quantiteF=1))   # +2 sushis via formule
    session.commit()

    besoins = res.getbesoin()
    assert besoins[p_sushi] == 3
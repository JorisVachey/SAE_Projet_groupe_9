from .app import db
from flask_login import UserMixin

class Restauratrice(UserMixin, db.Model):
    __tablename__ = "RESTAURATRICE"

    idRest = db.Column(db.Integer, primary_key=True)
    nomRest = db.Column(db.String(50))
    prenomRest = db.Column(db.String(50))
    numtelRest = db.Column(db.String(50))
    mdp = db.Column(db.String(50))

    def __init__(self, idRest, nomRest, prenomRest, numtelRest, mdp):
        self.idRest = idRest
        self.nomRest = nomRest
        self.prenomRest = prenomRest
        self.numtelRest = numtelRest
        self.mdp = mdp

    def __repr__(self):
        return f"<Restauratrice(id={self.idRest}, nom={self.nomRest}, prenom={self.prenomRest})>"
    
    def get_id(self):
        return f"resto-{self.idRest}"

class Client(UserMixin, db.Model):
    __tablename__ = "CLIENT"

    numtelCli = db.Column(db.String(50), primary_key=True)
    pseudonyme = db.Column(db.String(50))
    mdp = db.Column(db.String(500))
    est_banni = db.Column(db.Boolean)
    pts_fidelite = db.Column(db.Integer)

    reservations = db.relationship("Reservation", backref="client")

    def __init__(self, numtelCli, pseudonyme, mdp, est_banni=False, pts_fidelite=0):
        self.numtelCli = numtelCli
        self.pseudonyme = pseudonyme
        self.mdp = mdp
        self.est_banni = est_banni
        self.pts_fidelite = pts_fidelite

    def __repr__(self):
        return f"<Client(numtel={self.numtelCli}, pseudo={self.pseudonyme})>"
    
    def get_id(self):
        return f"client-{self.numtelCli}"


class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    idR = db.Column(db.Integer, primary_key=True)
    numtelCli = db.Column(db.String(50), db.ForeignKey("CLIENT.numtelCli"))
    dateR = db.Column(db.Date)
    nb_couverts = db.Column(db.Integer)
    sur_place = db.Column(db.Boolean)
    statut = db.Column(db.String(50))

    formules = db.relationship("ContenirF", backref="reservation")
    plats = db.relationship("ContenirP", backref="reservation")

    def __init__(self, idR, numtelCli, dateR, nb_couverts, sur_place, statut):
        self.idR = idR
        self.numtelCli = numtelCli
        self.dateR = dateR
        self.nb_couverts = nb_couverts
        self.sur_place = sur_place
        self.statut = statut

    def __repr__(self):
        return f"<Reservation(id={self.idR}, client={self.numtelCli}, date={self.dateR})>"

class Formule(db.Model):
    __tablename__ = "FORMULE"

    idF = db.Column(db.Integer, primary_key=True)
    nomF = db.Column(db.String(50))
    prixF = db.Column(db.Numeric(10, 2))

    plats = db.relationship("Composer", backref="formule")
    reservations = db.relationship("ContenirF", backref="formule")

    def __init__(self, idF, nomF, prixF):
        self.idF = idF
        self.nomF = nomF
        self.prixF = prixF

    def __repr__(self):
        return f"<Formule(id={self.idF}, nom={self.nomF}, prix={self.prixF})>"

class Type_plat(db.Model):
    __tablename__ = "TYPE_PLAT"

    idTp = db.Column(db.Integer, primary_key=True)
    nomTp = db.Column(db.String(50))
    descriptionTp = db.Column(db.String(50))
    cheminImg = db.Column(db.String(50))

    def __init__(self, idTp, nomTp, descriptionTp, cheminImg):
        self.idTp = idTp
        self.nomTp = nomTp
        self.descriptionTp = descriptionTp
        self.cheminImg = cheminImg

    def __repr__(self):
        return f"<type plat(id={self.idTp}, nom={self.nomTp}>"

class Plat(db.Model):
    __tablename__ = "PLAT"

    idP = db.Column(db.Integer, primary_key=True)
    nomP = db.Column(db.String(50))
    idTp = db.Column(db.Integer, db.ForeignKey("TYPE_PLAT.idTp"))
    prixP = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer)
    stockInit = db.Column(db.Integer)
    cheminImg = db.Column(db.String(50))
    descriptionP = db.Column(db.String(50))

    formules = db.relationship("Composer", backref="plat")
    reservations = db.relationship("ContenirP", backref="plat")

    def __init__(self, idP, nomP, idTp, prixP, stock, stockInit,cheminImg, descriptionP):
        self.idP = idP
        self.nomP = nomP
        self.idTp = idTp
        self.prixP = prixP
        self.stock = stock
        self.stockInit = stockInit
        self.cheminImg = cheminImg
        self.descriptionP = descriptionP

    def __repr__(self):
        return f"<Plat(id={self.idP}, nom={self.nomP}, type id={self.idTp}, prix={self.prixP})>"


class Composer(db.Model):
    __tablename__ = "COMPOSER"

    idF = db.Column(db.Integer, db.ForeignKey("FORMULE.idF"), primary_key=True)
    idP = db.Column(db.Integer, db.ForeignKey("PLAT.idP"), primary_key=True)
    quantiteC = db.Column(db.Integer)

    def __init__(self, idF, idP, quantiteC):
        self.idF = idF
        self.idP = idP
        self.quantiteC = quantiteC

    def __repr__(self):
        return f"<Composer(formule={self.idF}, plat={self.idP}, qte={self.quantiteC})>"


class ContenirF(db.Model):
    __tablename__ = "CONTENIR_F"

    idR = db.Column(db.Integer, db.ForeignKey("RESERVATION.idR"), primary_key=True)
    idF = db.Column(db.Integer, db.ForeignKey("FORMULE.idF"), primary_key=True)
    quantiteF = db.Column(db.Integer)

    def __init__(self, idR, idF, quantiteF):
        self.idR = idR
        self.idF = idF
        self.quantiteF = quantiteF

    def __repr__(self):
        return f"<ContenirF(reservation={self.idR}, formule={self.idF}, qte={self.quantiteF})>"


class ContenirP(db.Model):
    __tablename__ = "CONTENIR_P"

    idR = db.Column(db.Integer, db.ForeignKey("RESERVATION.idR"), primary_key=True)
    idP = db.Column(db.Integer, db.ForeignKey("PLAT.idP"), primary_key=True)
    quantiteP = db.Column(db.Integer)

    def __init__(self, idR, idP, quantiteP):
        self.idR = idR
        self.idP = idP
        self.quantiteP = quantiteP

    def __repr__(self):
        return f"<ContenirP(reservation={self.idR}, plat={self.idP}, qte={self.quantiteP})>"

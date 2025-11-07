from .app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "USER"

    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numtelUser = db.Column(db.String(50), unique=True)
    pseudonyme = db.Column(db.String(50))
    mdp = db.Column(db.String(500))
    est_banni = db.Column(db.Boolean, default=False)
    pts_fidelite = db.Column(db.Integer, default=0)
    est_admin = db.Column(db.Boolean, default=False)

    def __init__(self, numtelUser, pseudonyme, mdp, est_banni=False, pts_fidelite=0, est_admin=False):
        self.numtelUser = numtelUser
        self.pseudonyme = pseudonyme
        self.mdp = mdp
        self.est_banni = est_banni
        self.pts_fidelite = pts_fidelite
        self.est_admin = est_admin

    def __repr__(self):
        return f"<User(id={self.idUser}, pseudo={self.pseudonyme}, admin={self.est_admin})>"

    def get_id(self):
        return str(self.idUser)


class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    idR = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, db.ForeignKey("USER.idUser"), nullable=False)
    dateR = db.Column(db.Date)
    nb_couverts = db.Column(db.Integer)
    sur_place = db.Column(db.Boolean)
    statut = db.Column(db.String(50))

    formules = db.relationship("ContenirF", backref="reservation", cascade="all, delete-orphan")
    plats = db.relationship("ContenirP", backref="reservation", cascade="all, delete-orphan")
    user = db.relationship("User", backref=db.backref("reservations"))

    def get_total(self):
        total = 0
        for cp in self.plats:
            total += cp.quantiteP * cp.plat.prixP
        for cf in self.formules:
            total += cf.quantiteF * cf.formule.prixF
        return total

    def __init__(self, idUser, dateR, nb_couverts, sur_place, statut):
        self.idUser = idUser
        self.dateR = dateR
        self.nb_couverts = nb_couverts
        self.sur_place = sur_place
        self.statut = statut

    def __repr__(self):
        return f"<Reservation(id={self.idR}, user={self.numtelUser}, date={self.dateR})>"

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

    idP = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nomP = db.Column(db.String(50))
    idTp = db.Column(db.Integer, db.ForeignKey("TYPE_PLAT.idTp"))
    prixP = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer)
    stockInit = db.Column(db.Integer)
    cheminImg = db.Column(db.String(50))
    descriptionP = db.Column(db.String(50))

    compositions = db.relationship('Composer',backref='plat', cascade='all, delete-orphan', passive_deletes=True)
    reservations = db.relationship("ContenirP", backref="plat", passive_deletes=True)
    type = db.relationship("Type_plat", backref="plat", passive_deletes=True)


    def __init__(self, nomP, idTp, prixP, stock,cheminImg, descriptionP):
        self.nomP = nomP
        self.idTp = idTp
        self.prixP = prixP
        self.stock = stock
        self.cheminImg = cheminImg
        self.descriptionP = descriptionP

    def __repr__(self):
        return f"<Plat(id={self.idP}, nom={self.nomP}, type id={self.idTp}, prix={self.prixP})>"


class Restriction(db.Model):
    __tablename__ = "RESTRICTION"

    nomA = db.Column(db.String(50), primary_key=True)

    plats = db.relationship("ContenirR", backref="restriction")

    def __init__(self, nomA):
        self.nomA = nomA

    def __repr__(self):
        return f"<Restriction(nom={self.nomA})>"


class ContenirR(db.Model):
    __tablename__ = "CONTENIR_R"
    
    idP = db.Column(db.Integer, db.ForeignKey("PLAT.idP", ondelete="CASCADE"), primary_key=True)
    nomA = db.Column(db.String(50), db.ForeignKey("RESTRICTION.nomA"), primary_key=True)

    def __init__(self, idP, nomA):
        self.idP = idP
        self.nomA = nomA

    def __repr__(self):
        return f"<ContenirR(plat={self.idP}, restriction={self.nomA})>"


class Composer(db.Model):
    __tablename__ = "COMPOSER"

    idF = db.Column(db.Integer, db.ForeignKey("FORMULE.idF"), primary_key=True)
    idP = db.Column(db.Integer, db.ForeignKey('PLAT.idP', ondelete='CASCADE'),primary_key=True)
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
    idP = db.Column(db.Integer, db.ForeignKey("PLAT.idP", ondelete='CASCADE'), primary_key=True)
    quantiteP = db.Column(db.Integer)

    def __init__(self, idR, idP, quantiteP):
        self.idR = idR
        self.idP = idP
        self.quantiteP = quantiteP

    def __repr__(self):
        return f"<ContenirP(reservation={self.idR}, plat={self.idP}, qte={self.quantiteP})>"

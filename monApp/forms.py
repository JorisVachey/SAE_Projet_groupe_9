from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField , FloatField , PasswordField, IntegerField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired,Length
from .models import *
from hashlib import sha256


class RegisterForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    def get_registered_user(self):
        user = Client.query.get(self.numtel.data)
        if user is not None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        newClient = Client(numtelCli=self.numtel.data, pseudonyme=self.pseudonyme.data, mdp=passwd)
        return newClient

class LoginForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    def get_authenticated_user(self):
        user = Client.query.get(self.numtel.data)
        if not user:
            user = Restauratrice.query.filter_by(numtelRest=self.numtel.data).first()
        if not user:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else None

class SansCompteclientForm(FlaskForm):
    numtelCli = StringField('Numéro de téléphone', validators=[DataRequired()])
    valider = SubmitField('Valider')

class CompteclientForm(FlaskForm):
    numtelCli = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired()])
    valider = SubmitField('Valider')

class restauratriceForm(FlaskForm):
    idRest = StringField('Identifiant', validators=[DataRequired()])
    nomRest = StringField('Nom', validators=[DataRequired()])
    prenomRest = StringField('Prénom', validators=[DataRequired()])
    valider = SubmitField('Valider')




class ReservationForm(FlaskForm):
    idR = IntegerField('ID de la réservation', validators=[DataRequired()])
    numtelCli = StringField('Numéro de téléphone du client', validators=[DataRequired(), Length(max=50)])
    dateR = DateField('Date de réservation', validators=[DataRequired()], format='%Y-%m-%d')
    nb_couverts = IntegerField('Nombre de couverts', validators=[DataRequired()])
    sur_place = BooleanField('Sur place ?')
    statut = StringField('Statut', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Créer la réservation')

class formuleForm(FlaskForm):
    idF = IntegerField('ID de la formule', validators=[DataRequired()])
    idP = IntegerField('ID du plat', validators=[DataRequired()])
    nomF = StringField('Nom de la formule', validators=[DataRequired(), Length(max=50)])
    prixF = FloatField('Prix de la formule', validators=[DataRequired()])
    submit = SubmitField('Créer la formule')

class platForm(FlaskForm):
    idP = IntegerField('ID du plat', validators=[DataRequired()])
    nomP = StringField('Nom du plat', validators=[DataRequired(), Length(max=50)])
    typeP = StringField('Type de plat', validators=[DataRequired(), Length(max=50)])
    prixP = FloatField('Prix du plat', validators=[DataRequired()])
    stock = IntegerField('Stock du plat', validators=[DataRequired()])
    descriptionP = StringField('Description du plat', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Créer le plat')

class composerForm(FlaskForm):
    idF = IntegerField('ID de la formule', validators=[DataRequired()])
    idp = IntegerField('ID du plat', validators=[DataRequired()])
    quantiteC = IntegerField('Quantité contenue dans formule', validators=[DataRequired()])
    submit = SubmitField('Créer la formule')

class contenirfForm(FlaskForm):
    idF = IntegerField('ID de la formule', validators=[DataRequired()])
    idR = IntegerField('ID de la réservation', validators=[DataRequired()])
    quantiteF = IntegerField('Quantité de formule', validators=[DataRequired()])
    submit = SubmitField('Ajouter la formule au panier')

class contenirpForm(FlaskForm):
    idP = IntegerField('ID du plat', validators=[DataRequired()])
    idR = IntegerField('ID de la réservation', validators=[DataRequired()])
    quantiteP = IntegerField('Quantité du plat', validators=[DataRequired()])
    submit = SubmitField('Ajouter le plat au panier')
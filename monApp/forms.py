from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, IntegerField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Length
from .models import User
from hashlib import sha256


class RegisterForm(FlaskForm):
    """form pour s'inscrire

    Args:
        FlaskForm (_type_): _description_

    Returns:
        _type_: _description_
    """
    numtel = StringField('Numéro de téléphone',
                         validators=[DataRequired(),
                                     Length(max=10)])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

    def get_registered_user(self):
        user = User.query.get(self.numtel.data)
        if user:
            print('Utilisateur inexistant')
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        new_client = User(numtelUser=self.numtel.data,
                         pseudonyme=self.pseudonyme.data,
                         mdp=passwd)
        return new_client


class LoginForm(FlaskForm):
    """form pour se connecter

    Args:
        FlaskForm (_type_): _description_

    Returns:
        _type_: _description_
    """
    numtel = StringField('Numéro de téléphone',
                         validators=[DataRequired(),
                                     Length(max=10)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

    def get_authenticated_user(self):
        user = User.query.filter_by(numtelUser=self.numtel.data).first()
        if user is None:
            print('--Utilisateur introuvable--')
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else None


class SansCompteclientForm(FlaskForm):
    """form pour commander sans avoir de compte

    Args:
        FlaskForm (_type_): _description_
    """
    numtel_user = StringField('Numéro de téléphone', validators=[DataRequired()])
    valider = SubmitField('Valider')


class CompteuserForm(FlaskForm):
    """form pour voir et modifier les infos du compte

    Args:
        FlaskForm (_type_): _description_
    """
    numtel_user = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired()])
    valider = SubmitField('Valider')


class ReservationForm(FlaskForm):
    """form pour la reservation

    Args:
        FlaskForm (_type_): _description_
    """
    idR = IntegerField('ID de la réservation', validators=[DataRequired()])
    numtel_user = StringField('Numéro de téléphone du client',
                             validators=[DataRequired(),
                                         Length(max=50)])
    dateR = DateField('Date de réservation',
                      validators=[DataRequired()],
                      format='%Y-%m-%d')
    nb_couverts = IntegerField('Nombre de couverts',
                               validators=[DataRequired()])
    sur_place = BooleanField('Sur place ?')
    statut = StringField('Statut', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Créer la réservation')


class FormuleForm(FlaskForm):
    """form pour les formules

    Args:
        FlaskForm (_type_): _description_
    """
    idF = IntegerField('ID de la formule', validators=[DataRequired()])
    idP = IntegerField('ID du plat', validators=[DataRequired()])
    nomF = StringField('Nom de la formule',
                       validators=[DataRequired(),
                                   Length(max=50)])
    prixF = FloatField('Prix de la formule', validators=[DataRequired()])
    cheminImg= StringField("Image de la formule")
    submit = SubmitField('Créer la formule')
    


class PlatForm(FlaskForm):
    """form pout les plats

    Args:
        FlaskForm (_type_): _description_
    """
    idP = IntegerField('ID du plat', validators=[DataRequired()])
    nomP = StringField('Nom du plat',
                       validators=[DataRequired(),
                                   Length(max=50)])
    typeP = StringField('Type de plat',
                        validators=[DataRequired(),
                                    Length(max=50)])
    prixP = FloatField('Prix du plat', validators=[DataRequired()])
    stock = IntegerField('Stock du plat', validators=[DataRequired()])
    descriptionP = StringField('Description du plat',
                               validators=[DataRequired(),
                                           Length(max=50)])
    submit = SubmitField('Créer le plat')


class ComposerForm(FlaskForm):
    """form pout ma composition de formule

    Args:
        FlaskForm (_type_): _description_
    """
    idF = IntegerField('ID de la formule', validators=[DataRequired()])
    idp = IntegerField('ID du plat', validators=[DataRequired()])
    quantiteC = IntegerField('Quantité contenue dans formule',
                             validators=[DataRequired()])
    submit = SubmitField('Créer la formule')


class ContenirfForm(FlaskForm):
    """form pour le nombre de formule

    Args:
        FlaskForm (_type_): _description_
    """
    idF = IntegerField('ID de la formule', validators=[DataRequired()])
    idR = IntegerField('ID de la réservation', validators=[DataRequired()])
    quantiteF = IntegerField('Quantité de formule', validators=[DataRequired()])
    submit = SubmitField('Ajouter la formule au panier')


class ContenirpForm(FlaskForm):
    """form pour le nombre de plat

    Args:
        FlaskForm (_type_): _description_
    """
    idP = IntegerField('ID du plat', validators=[DataRequired()])
    idR = IntegerField('ID de la réservation', validators=[DataRequired()])
    quantiteP = IntegerField('Quantité du plat', validators=[DataRequired()])
    submit = SubmitField('Ajouter le plat au panier')
